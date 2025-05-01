import { HttpClient } from '@angular/common/http';
import { Component } from '@angular/core';
import { FormBuilder, FormGroup, ReactiveFormsModule, Validators } from '@angular/forms';
import { ProductInputComponent } from "../../components/product-input/product-input.component";
import { CommonModule } from '@angular/common';

interface Product {
  id: number;
  name: string;
  description: string;
  category: string;
  subcategory: string;
  width: string;
  height: string;
  length: string;
  weight: string;
  quantity: number;
  is_fragile: boolean;
  requires_refrigeration: boolean;
  total_weight: number;
}

interface Packaging {
  ai?: {
    optimalSize?: string;
    material?: string;
    requiredPadding?: string;
    efficiency?: string;
  };
  manual?: {
    containerSize?: string;
    material?: string;
    padding?: string;
  };
}

interface FreightOption {
  type: string;
  costPerKg: string;
  deliveryTime: string;
  co2Impact: string;
}

@Component({
  selector: 'app-products-page',
  templateUrl: './products-page.component.html',
  styleUrls: ['./products-page.component.scss'],
  imports: [ProductInputComponent, CommonModule, ReactiveFormsModule]
})
export class ProductsPageComponent {
  identifiedProduct: Product | null = null;
  packaging: Packaging | null = null;
  freightOptions: FreightOption[] = [];
  packagingForm: FormGroup;

  primaryColor = '#19194b';
  secondaryColor = '#1c3f93';
  accentColor = '#eb711b';
  highlightColor = '#d9e11c';
  textColor = '#ffffff';
  backgroundColor = '#f4f4f4';

  constructor(
    private http: HttpClient,
    private fb: FormBuilder
  ) {
    this.packagingForm = this.fb.group({
      containerSize: ['', [
        Validators.required,
        Validators.pattern(/^\d+×\d+×\d+$/)
      ]],
      material: ['cardboard', Validators.required],
      padding: ['basic', Validators.required]
    });
  }

  processImageInput(input: { url?: string; file?: File }) {
    if (input.url) {
      this.processImageUrl(input.url);
    } else if (input.file) {
      this.processImageFile(input.file);
    }
  }

  private processImageUrl(imageUrl: string) {
    this.http.post<{ product: Product }>('http://127.0.0.1:8000/api/detect-product/', { image_url: imageUrl })
      .subscribe({
        next: (response) => {
          this.identifiedProduct = response.product; // ✅ Correct: access nested product
          this.generateMockData(response.product); // Pass the actual product data
        },
        error: (error) => {
          console.error('Error:', error);
          this.identifiedProduct = null;
        }
      });
  }

  private processImageFile(file: File) {
    const formData = new FormData();
    formData.append('image', file);

    this.http.post<Product>('http://127.0.0.1:8000/api/detect-product/', formData)
      .subscribe({
        next: (product) => {
          this.identifiedProduct = product;
          this.generateMockData(product);
        },
        error: (error) => {
          console.error('Error:', error);
          this.identifiedProduct = null;
        }
      });
  }

  private generateMockData(product: Product) {
    this.packaging = {
      ai: {
        optimalSize: this.calculateTotalDimensions(product),
        material: product.is_fragile ? 'Double-walled cardboard' : 'Standard cardboard',
        requiredPadding: product.is_fragile ? '15mm premium padding' : '5mm basic foam',
        efficiency: '92% space utilization'
      }
    };

    this.freightOptions = [
      {
        type: '🚢 Ocean Shipping',
        costPerKg: '$1.20/kg',
        deliveryTime: '18-25 days',
        co2Impact: 'Low (0.5kg CO₂/kg)'
      },
      {
        type: '✈️ Air Freight',
        costPerKg: '$4.80/kg',
        deliveryTime: '3-5 days',
        co2Impact: 'High (8.2kg CO₂/kg)'
      },
      {
        type: '🚚 Ground Transport',
        costPerKg: '$0.80/kg',
        deliveryTime: '7-10 days',
        co2Impact: 'Medium (2.1kg CO₂/kg)'
      }
    ];
  }

  generateOptimalPackaging() {
    if (this.identifiedProduct) {
      this.packaging = {
        ...this.packaging,
        ai: {
          optimalSize: this.calculateTotalDimensions(this.identifiedProduct),
          material: this.identifiedProduct.is_fragile ? 
            'Double-walled cardboard' : 'Standard cardboard',
          requiredPadding: this.identifiedProduct.is_fragile ? 
            '15mm premium padding' : '5mm basic foam',
          efficiency: '95% space efficiency'
        }
      };
    }
  }

  applyManualPackaging() {
    if (this.packagingForm.valid) {
      this.packaging = {
        ...this.packaging,
        manual: {
          containerSize: this.packagingForm.value.containerSize,
          material: this.packagingForm.value.material,
          padding: this.packagingForm.value.padding
        }
      };
      this.packagingForm.reset();
    }
  }

  private calculateTotalDimensions(product: Product): string {
    const width = parseFloat(product.width) || 0;
    const height = parseFloat(product.height) || 0;
    const length = parseFloat(product.length) || 0;
    const volume = width * height * length;
    return volume > 0 ? `${volume.toFixed(2)} cm³` : 'N/A';
  }
}