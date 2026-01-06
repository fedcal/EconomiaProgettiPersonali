import { Routes } from '@angular/router';

export const TASKS_ROUTES: Routes = [
  {
    path: '',
    loadComponent: () => import('./task-list.component').then(m => m.TaskListComponent)
  },
  {
    path: 'new',
    loadComponent: () => import('./task-form.component').then(m => m.TaskFormComponent)
  },
  {
    path: 'edit/:id',
    loadComponent: () => import('./task-form.component').then(m => m.TaskFormComponent)
  }
];
