import { Component } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { ProductInputComponent } from '../../components/product-input/product-input.component';

@Component({
  selector: 'app-test',
  standalone: true,
  imports: [ProductInputComponent],
  templateUrl: './test.component.html',
  styleUrls: ['./test.component.scss']
})
export class TestComponent {
  constructor(private http: HttpClient) {}

  processImageInput(input: { url?: string, file?: File }) {
    if (input.url) {
      this.processImageUrl(input.url);
    } else if (input.file) {
      this.processImageFile(input.file);
    }
  }

  private processImageUrl(imageUrl: string) {
    this.http.post('http://127.0.0.1:8000/api/detect-product/', { image_url: imageUrl })
      .subscribe({
        next: (response: any) => {
          console.log('URL Detection results:', response.detected_class);
        },
        error: (error) => {
          console.error('URL Error:', error);
        }
      });
  }

  private processImageFile(file: File) {
    const formData = new FormData();
    formData.append('image', file);

    this.http.post('http://127.0.0.1:8000/api/detect-product/', formData)
      .subscribe({
        next: (response: any) => {
          console.log('File Detection results:', response.detected_class);
        },
        error: (error) => {
          console.error('File Error:', error);
        }
      });
  }
}