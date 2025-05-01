import numpy as np
import pandas as pd
from py3dbp import Packer, Bin, Item
from multiprocessing import Process, Pool, Queue
from itertools import permutations
from typing import Any, Dict


def pack_worker(packer, q):
    packer.pack()
    q.put(packer)

def pack_box(args):
    def division_zero(x, y):
        return x // y if y else 0

    item_x, item_y, item_z, item_wt, item_vol, item_id, item_name, bin_x, bin_y, bin_z, bin_wt, bin_vol = args
    item_attributes = [item_x, item_y, item_z]
    bin_attributes = [bin_x, bin_y, bin_z]

    wht_max_qty = division_zero(bin_wt, item_wt)
    vol_max_qty = division_zero(bin_vol, item_vol)

    if wht_max_qty == 0 or vol_max_qty == 0:
        max_qty = 0
    else:
        packer = Packer()
        packer.add_bin(Bin("LB", bin_x, bin_y, bin_z, max_weight=bin_wt))
        max_b_load = int(min(wht_max_qty, vol_max_qty))

        for i in range(max_b_load):
            packer.add_item(Item(f"item_{i}", item_x, item_y, item_z, item_wt))

        q = Queue()
        pack_process = Process(target=pack_worker, args=(packer, q))
        pack_process.start()
        pack_process.join(timeout=0.8)

        if pack_process.is_alive():
            pack_process.terminate()
            pack_process.join()
            side_load = [int(j / i) for i, j in zip(item_attributes, bin_attributes)]
            load_qty = np.prod(side_load)
            max_qty = min(load_qty, wht_max_qty)
        else:
            packer = q.get()
            max_qty = len(packer.bins[0].items)

    fill_rate = np.round((max_qty * item_vol / bin_vol) * 100, decimals=1) if bin_vol else 0.0
    return max_qty, fill_rate


def permute_item_orientations(args):
    # Unpack args
    item_x, item_y, item_z, item_wt, item_vol,  item_id, item_name, bin_x, bin_y, bin_z, bin_wt, bin_vol = args
    item_attributes = [item_x, item_y, item_z]
    bin_attributes = [bin_x, bin_y, bin_z]

    # Tracking variables
    qty_results_list = []
    fill_results_list = []

    # Determine permutations of item dimensions
    item_perms = list(permutations(item_attributes[:3]))

    # Loop through permutations of item dimensions
    for item_perm in item_perms:
        qty_result, fill_rate = pack_box(item_perm + args[3:])
        qty_results_list.append(qty_result)
        fill_results_list.append(fill_rate)

    return qty_results_list, fill_results_list, item_perms


def try_container_n(boxes, item):
    """
    Determine fill for item in bin N. This function is called for each item in the list.

    Parameters:
    row (Dict[str, Any]): JSON object representing the item (with item attributes like length, width, etc.)

    Returns:
    row (Dict[str, Any]): Original row object, with added container fill results for the given item
    """
    # Pull out item arguments from the JSON object: item_args = (item_x, item_y, item_z, item_wt, item_vol)
    item_args = (
        item["length"],   # Item length
        item["width"],    # Item width
        item["height"],   # Item height
        item["weight"],   # Item weight
        item["volume"],   # Item volume
        item["id"],
        item["name"],
    )

    # List of bins (hardcoded here, but could come from elsewhere)
    bins_args = boxes  # Assuming 'boxes' is a list of bins like the one in your previous code
    bin_fills = []

    # Loop through each bin to calculate item fits
    for bin in bins_args:
        # Extract bin parameters: (box_length, box_width, box_height, fill_capacity, bin_vol)
        bin_args = (
            bin["length"],
            bin["width"],
            bin["height"],
            bin["fill_capacity"],
            bin["volume"],
        )

        # Combine item and bin arguments into a single tuple
        args = item_args + bin_args

        # Pass combined args to the permute_item_orientations function
        qty_results_list, fill_results_list, item_perms = permute_item_orientations(args)

          # Find the best quantity and fill percentage
        best_qty = max(qty_results_list)  # Assume best quantity is the maximum
        best_fill_pct = max(fill_results_list)  # Assume best fill percentage is the maximum

        # Store the results for the current bin
        single_bin_fill = {
            "box_id": bin["name"],
            "qty_results": qty_results_list,
            "fill_pct_results": fill_results_list,
            "item_perms": item_perms,  # Add item permutations to the dictionary
            "best_qty": best_qty,  # Add best_qty to the dictionary
            "best_fill_pct": best_fill_pct,  # Add best_fill_pct to the dictionary
        }

        bin_fills.append(single_bin_fill)

    # Attach the bin filling results to the original row object
    item["bin_fills"] = bin_fills
    return item