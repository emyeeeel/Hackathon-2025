import { HttpClient } from '@angular/common/http';
import { Component } from '@angular/core';
import { ProductInputComponent } from "../../components/product-input/product-input.component";

@Component({
  selector: 'app-products-page',
  imports: [ProductInputComponent],
  templateUrl: './products-page.component.html',
  styleUrls: ['./products-page.component.scss']
})
export class ProductsPageComponent {
  identifiedProduct: any;
  receivedInput: { url?: string; file?: File } | null = null; // Variable to store the input

  constructor(private http: HttpClient) {}

  processImageInput(input: { url?: string; file?: File }) {
    this.receivedInput = input; // Save the input to the variable
    console.log('Received Input:', input); // Debugging log

    if (input.url) {
      this.processImageUrl(input.url);
    } else if (input.file) {
      this.processImageFile(input.file);
    }
  }

  private processImageUrl(imageUrl: string) {
    console.log('Sending URL to backend:', imageUrl);
    this.http.post('http://127.0.0.1:8000/api/detect-product/', { image_url: imageUrl })
      .subscribe({
        next: (response: any) => {
          console.log('URL Detection results:', response);
          this.identifiedProduct = response;
        },
        error: (error) => {
          console.error('URL Error:', error);
        }
      });
  }

  private processImageFile(file: File) {
    const formData = new FormData();
    formData.append('image', file);

    console.log('Sending file to backend:', file.name);
    this.http.post('http://127.0.0.1:8000/api/detect-product/', formData)
      .subscribe({
        next: (response: any) => {
          console.log('File Detection results:', response);
          this.identifiedProduct = response;
        },
        error: (error) => {
          console.error('File Error:', error);
        }
      });
  }
}
