import { ComponentFixture, TestBed } from '@angular/core/testing';

import { ProductInputComponent } from './product-input.component';

describe('ProductInputComponent', () => {
  let component: ProductInputComponent;
  let fixture: ComponentFixture<ProductInputComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [ProductInputComponent]
    })
    .compileComponents();

    fixture = TestBed.createComponent(ProductInputComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
