import { Component } from '@angular/core';
import { PackagingRecommenderComponent } from "../../components/packaging-recommender/packaging-recommender.component";

@Component({
  selector: 'app-packaging-page',
  imports: [PackagingRecommenderComponent],
  templateUrl: './packaging-page.component.html',
  styleUrl: './packaging-page.component.scss'
})
export class PackagingPageComponent {

}
