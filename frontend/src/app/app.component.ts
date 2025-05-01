import { Component } from '@angular/core';
import { RouterOutlet } from '@angular/router';
import { ProductInputComponent } from './components/product-input/product-input.component';

@Component({
  selector: 'app-root',
  imports: [RouterOutlet, ProductInputComponent],
  templateUrl: './app.component.html',
  styleUrl: './app.component.scss'
})
export class AppComponent {
  title = 'frontend';
}
