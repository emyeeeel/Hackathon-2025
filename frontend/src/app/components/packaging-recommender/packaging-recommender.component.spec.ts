import { ComponentFixture, TestBed } from '@angular/core/testing';

import { PackagingRecommenderComponent } from './packaging-recommender.component';

describe('PackagingRecommenderComponent', () => {
  let component: PackagingRecommenderComponent;
  let fixture: ComponentFixture<PackagingRecommenderComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [PackagingRecommenderComponent]
    })
    .compileComponents();

    fixture = TestBed.createComponent(PackagingRecommenderComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
