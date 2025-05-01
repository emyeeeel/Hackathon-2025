
import numpy as np
#SAMPLE INPUTS:
# product = {
#     "id": 1,
#     "name": "Kettle",
#     "length": 16.0,
#     "width": 23.0,
#     "height": 21.0,
#     "weight": 1.0,
#     "quantity":65,
#     "volume": 16.0 * 23.0 * 21.0 
# }
# selected_box = {
#     "box_id": "B0005",
#     "fill_percent": 100.0,
#     "fill_quantity": 8,
#     "item_perm": (16.0, 23.0, 21.0),
# }



def calculate_no_of_boxes(product, selected_box):
  #Calculate the number of boxes that will be used based on selected box
  no_of_packed_boxes = np.floor(product["quantity"] / selected_box["fill_quantity"])

  #Remainder from what was not able to be put in the box
  no_of_unpacked_products = product["quantity"] % selected_box["fill_quantity"] 

  return no_of_packed_boxes, no_of_unpacked_products


def select_box(product, selected_box):
  no_of_packed_boxes, no_of_unpacked_products = calculate_no_of_boxes(product, selected_box)
  box_recommendations = try_container_n(boxes, product) 
  box_quantities = []
  for box in box_recommendations["bin_fills"]:
    box_quantities.append({"box_id": box["box_id"], "best_qty": box["best_qty"]}) 
  
  # Filter based on minimum quantity
  filtered_box_quantities = [box for box in box_quantities if box["best_qty"] >= no_of_unpacked_products]
  # Sort based on best quantity in descending order
  sorted_box_quantities = sorted(filtered_box_quantities, key=lambda x: x["best_qty"])
  box_for_remaining_products = sorted_box_quantities[0]

  return box_for_remaining_products


def get_packed_boxes(product, selected_box):
  no_of_packed_boxes, no_of_unpacked_products = calculate_no_of_boxes(product, selected_box)
  total_packed_boxes = []
  for i in range(int(no_of_packed_boxes)):
    packed_box = {"box": selected_box['box_id'], 
                  "product": product, 
                  "product_quantity": selected_box["fill_quantity"], 
                  "fill_percent": selected_box["fill_percent"]}
    total_packed_boxes.append(packed_box)
    
  # if no_of_unpacked_products != 0:
  #   box_for_remaining_products = select_box(product, selected_box)
  #   packed_box = {"box": selected_box['box_id'], 
  #                 "product": product, 
  #                 "product_quantity": selected_box["fill_quantity"], 
  #                 "fill_percent": selected_box["fill_percent"]}

  # total_packed_boxes.append(box_for_remaining_products)
  return total_packed_boxes