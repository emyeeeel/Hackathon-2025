import { Component } from '@angular/core';
import { HttpClient } from '@angular/common/http';

@Component({
  selector: 'app-test',
  templateUrl: './test.component.html',
  styleUrls: ['./test.component.scss']
})
export class TestComponent {
  constructor(private http: HttpClient) {}

  postImageUrl() {
    const imageUrl = 'https://www.smappliance.com/cdn/shop/products/10156876-KW-1362-1.7LE.KETTLE_800x.png?v=1620836331';

    this.http.post('http://127.0.0.1:8000/api/detect-product/', { image_url: imageUrl })
      .subscribe({
        next: (response: any) => {
          console.log('Detection results:', response.detected_class);
        },
        error: (error) => {
          console.error('Error:', error);
        },
        complete: () => {
          console.log('Request completed.');
        }
      });
  }
}
