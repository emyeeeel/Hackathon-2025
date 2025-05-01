import { Routes } from '@angular/router';
import { TestComponent } from './pages/test/test.component';
import { ProductsPageComponent } from './pages/products-page/products-page.component';
import { PackagingPageComponent } from './pages/packaging-page/packaging-page.component';

export const routes: Routes = [
    {
        path: 'test',
        component: TestComponent
    },
    {
        path: 'products',
        component: ProductsPageComponent
    },
    {
        path: 'packaging',
        component: PackagingPageComponent
    },
];
