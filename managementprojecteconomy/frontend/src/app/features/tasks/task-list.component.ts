import { Component, OnInit, inject, signal } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { ActivatedRoute, Router } from '@angular/router';
import { TaskService } from '../../core/services/task.service';
import { ProjectService } from '../../core/services/project.service';
import { Task } from '../../core/models/task.model';
import { Project } from '../../core/models/project.model';
import { TaskStatus } from '../../core/models/enums';

/**
 * Component for displaying and managing tasks
 */
@Component({
  selector: 'app-task-list',
  standalone: true,
  imports: [CommonModule, FormsModule],
  template: `
    <div class="task-list-container">
      <div class="header">
        <h1>Gestione Task</h1>
        <button class="btn-primary" (click)="createNewTask()">+ Nuovo Task</button>
      </div>

      <div class="project-selector" *ngIf="projects().length > 0">
        <label for="project-select">Progetto:</label>
        <select id="project-select" [(ngModel)]="selectedProjectId" (change)="onProjectChange()">
          <option value="">-- Tutti i progetti --</option>
          <option *ngFor="let project of projects()" [value]="project.id">
            {{ project.name }}
          </option>
        </select>
      </div>

      <div class="filters" *ngIf="selectedProjectId">
        <button
          *ngFor="let status of taskStatuses"
          class="filter-btn"
          [class.active]="selectedStatus === status"
          (click)="filterByStatus(status)">
          {{ getStatusLabel(status) }} ({{ getTaskCountByStatus(status) }})
        </button>
        <button
          class="filter-btn"
          [class.active]="selectedStatus === null"
          (click)="clearStatusFilter()">
          Tutti
        </button>
      </div>

      <div class="loading" *ngIf="loading()">Caricamento...</div>
      <div class="error" *ngIf="error()">{{ error() }}</div>

      <div class="tasks-grid" *ngIf="!loading() && !error()">
        <div *ngIf="filteredTasks().length === 0" class="no-tasks">
          Nessun task trovato. Crea il tuo primo task!
        </div>

        <div class="task-card" *ngFor="let task of filteredTasks()">
          <div class="task-header">
            <h3>{{ task.title }}</h3>
            <span class="task-status" [class]="'status-' + task.status.toLowerCase()">
              {{ getStatusLabel(task.status) }}
            </span>
          </div>

          <div class="task-meta">
            <span class="task-project">{{ task.projectName }}</span>
            <span class="task-tag" *ngIf="task.tag">🏷️ {{ task.tag }}</span>
          </div>

          <div class="task-description" *ngIf="task.description">
            {{ task.description }}
          </div>

          <div class="task-footer">
            <span class="task-date">Creato: {{ formatDate(task.createdAt) }}</span>
            <div class="task-actions">
              <button class="btn-edit" (click)="editTask(task)">✏️ Modifica</button>
              <button class="btn-delete" (click)="deleteTask(task)">🗑️ Elimina</button>
            </div>
          </div>
        </div>
      </div>
    </div>
  `,
  styles: [`
    .task-list-container {
      padding: 20px;
      max-width: 1200px;
      margin: 0 auto;
    }

    .header {
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-bottom: 30px;
    }

    h1 {
      margin: 0;
      font-size: 2rem;
      color: #2c3e50;
    }

    .btn-primary {
      background: #3498db;
      color: white;
      border: none;
      padding: 12px 24px;
      border-radius: 6px;
      cursor: pointer;
      font-size: 1rem;
      font-weight: 600;
      transition: background 0.3s;
    }

    .btn-primary:hover {
      background: #2980b9;
    }

    .project-selector {
      margin-bottom: 20px;
    }

    .project-selector label {
      margin-right: 10px;
      font-weight: 600;
    }

    .project-selector select {
      padding: 8px 12px;
      border: 1px solid #ddd;
      border-radius: 4px;
      font-size: 1rem;
    }

    .filters {
      display: flex;
      gap: 10px;
      margin-bottom: 20px;
      flex-wrap: wrap;
    }

    .filter-btn {
      padding: 8px 16px;
      border: 1px solid #ddd;
      background: white;
      border-radius: 4px;
      cursor: pointer;
      font-size: 0.9rem;
      transition: all 0.3s;
    }

    .filter-btn:hover {
      border-color: #3498db;
    }

    .filter-btn.active {
      background: #3498db;
      color: white;
      border-color: #3498db;
    }

    .loading, .error {
      text-align: center;
      padding: 40px;
      font-size: 1.2rem;
    }

    .error {
      color: #e74c3c;
    }

    .tasks-grid {
      display: grid;
      grid-template-columns: repeat(auto-fill, minmax(350px, 1fr));
      gap: 20px;
    }

    .no-tasks {
      grid-column: 1 / -1;
      text-align: center;
      padding: 60px;
      color: #7f8c8d;
      font-size: 1.1rem;
    }

    .task-card {
      background: white;
      border: 1px solid #e1e8ed;
      border-radius: 8px;
      padding: 20px;
      transition: all 0.3s;
      box-shadow: 0 2px 4px rgba(0,0,0,0.05);
    }

    .task-card:hover {
      box-shadow: 0 4px 12px rgba(0,0,0,0.1);
      transform: translateY(-2px);
    }

    .task-header {
      display: flex;
      justify-content: space-between;
      align-items: flex-start;
      margin-bottom: 12px;
    }

    .task-header h3 {
      margin: 0;
      font-size: 1.2rem;
      color: #2c3e50;
      flex: 1;
    }

    .task-status {
      padding: 4px 12px;
      border-radius: 12px;
      font-size: 0.8rem;
      font-weight: 600;
      white-space: nowrap;
    }

    .status-todo {
      background: #ecf0f1;
      color: #7f8c8d;
    }

    .status-in_progress {
      background: #fff3cd;
      color: #856404;
    }

    .status-completed {
      background: #d4edda;
      color: #155724;
    }

    .status-blocked {
      background: #f8d7da;
      color: #721c24;
    }

    .status-cancelled {
      background: #e2e3e5;
      color: #383d41;
    }

    .task-meta {
      display: flex;
      gap: 12px;
      margin-bottom: 12px;
      font-size: 0.9rem;
      color: #7f8c8d;
    }

    .task-tag {
      background: #ecf0f1;
      padding: 2px 8px;
      border-radius: 4px;
    }

    .task-description {
      margin-bottom: 16px;
      color: #34495e;
      line-height: 1.5;
    }

    .task-footer {
      display: flex;
      justify-content: space-between;
      align-items: center;
      border-top: 1px solid #ecf0f1;
      padding-top: 12px;
    }

    .task-date {
      font-size: 0.85rem;
      color: #95a5a6;
    }

    .task-actions {
      display: flex;
      gap: 8px;
    }

    .btn-edit, .btn-delete {
      padding: 6px 12px;
      border: none;
      border-radius: 4px;
      cursor: pointer;
      font-size: 0.85rem;
      transition: all 0.3s;
    }

    .btn-edit {
      background: #3498db;
      color: white;
    }

    .btn-edit:hover {
      background: #2980b9;
    }

    .btn-delete {
      background: #e74c3c;
      color: white;
    }

    .btn-delete:hover {
      background: #c0392b;
    }
  `]
})
export class TaskListComponent implements OnInit {
  private taskService = inject(TaskService);
  private projectService = inject(ProjectService);
  private router = inject(Router);
  private route = inject(ActivatedRoute);

  tasks = signal<Task[]>([]);
  filteredTasks = signal<Task[]>([]);
  projects = signal<Project[]>([]);
  loading = signal(true);
  error = signal<string | null>(null);

  selectedProjectId: string = '';
  selectedStatus: TaskStatus | null = null;

  taskStatuses: TaskStatus[] = [
    TaskStatus.TODO,
    TaskStatus.IN_PROGRESS,
    TaskStatus.COMPLETED,
    TaskStatus.BLOCKED,
    TaskStatus.CANCELLED
  ];

  ngOnInit(): void {
    this.loadProjects();
  }

  loadProjects(): void {
    this.projectService.getAll().subscribe({
      next: (data) => {
        this.projects.set(data);
        // If there's only one project, auto-select it
        if (data.length === 1) {
          this.selectedProjectId = data[0].id.toString();
          this.loadTasks();
        } else {
          this.loading.set(false);
        }
      },
      error: (err) => {
        this.error.set('Impossibile caricare i progetti. Backend non in esecuzione?');
        this.loading.set(false);
      }
    });
  }

  onProjectChange(): void {
    if (this.selectedProjectId) {
      this.loadTasks();
    } else {
      this.tasks.set([]);
      this.filteredTasks.set([]);
    }
  }

  loadTasks(): void {
    if (!this.selectedProjectId) return;

    this.loading.set(true);
    this.taskService.getByProjectId(+this.selectedProjectId).subscribe({
      next: (data) => {
        this.tasks.set(data);
        this.applyFilters();
        this.loading.set(false);
      },
      error: (err) => {
        this.error.set('Impossibile caricare i task.');
        this.loading.set(false);
      }
    });
  }

  filterByStatus(status: TaskStatus): void {
    this.selectedStatus = status;
    this.applyFilters();
  }

  clearStatusFilter(): void {
    this.selectedStatus = null;
    this.applyFilters();
  }

  applyFilters(): void {
    let filtered = this.tasks();
    if (this.selectedStatus !== null) {
      filtered = filtered.filter(t => t.status === this.selectedStatus);
    }
    this.filteredTasks.set(filtered);
  }

  getTaskCountByStatus(status: TaskStatus): number {
    return this.tasks().filter(t => t.status === status).length;
  }

  getStatusLabel(status: TaskStatus): string {
    const labels: Record<TaskStatus, string> = {
      [TaskStatus.TODO]: 'Da fare',
      [TaskStatus.IN_PROGRESS]: 'In corso',
      [TaskStatus.COMPLETED]: 'Completato',
      [TaskStatus.BLOCKED]: 'Bloccato',
      [TaskStatus.CANCELLED]: 'Annullato'
    };
    return labels[status];
  }

  formatDate(dateString: string): string {
    const date = new Date(dateString);
    return date.toLocaleDateString('it-IT', {
      year: 'numeric',
      month: 'short',
      day: 'numeric'
    });
  }

  createNewTask(): void {
    this.router.navigate(['/tasks/new']);
  }

  editTask(task: Task): void {
    this.router.navigate(['/tasks/edit', task.id]);
  }

  deleteTask(task: Task): void {
    if (confirm(`Sei sicuro di voler eliminare il task "${task.title}"?`)) {
      this.taskService.delete(task.id).subscribe({
        next: () => {
          this.loadTasks();
        },
        error: (err) => {
          alert('Errore durante l\'eliminazione del task.');
        }
      });
    }
  }
}
