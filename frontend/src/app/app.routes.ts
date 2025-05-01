import { Routes } from '@angular/router';
import { ProductsPageComponent } from './pages/products-page/products-page.component';
import { PackagingPageComponent } from './pages/packaging-page/packaging-page.component';

export const routes: Routes = [
    {
        path: '',
        component: ProductsPageComponent
    },
    {
        path: 'packaging',
        component: PackagingPageComponent
    },
];
