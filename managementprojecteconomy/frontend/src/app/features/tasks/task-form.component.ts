import { Component, OnInit, inject, signal } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormBuilder, FormGroup, ReactiveFormsModule, Validators } from '@angular/forms';
import { ActivatedRoute, Router } from '@angular/router';
import { TaskService } from '../../core/services/task.service';
import { ProjectService } from '../../core/services/project.service';
import { TaskRequest } from '../../core/models/task.model';
import { Project } from '../../core/models/project.model';
import { TaskStatus } from '../../core/models/enums';

/**
 * Component for creating and editing tasks
 */
@Component({
  selector: 'app-task-form',
  standalone: true,
  imports: [CommonModule, ReactiveFormsModule],
  template: `
    <div class="task-form-container">
      <div class="header">
        <h1>{{ isEditMode ? 'Modifica Task' : 'Nuovo Task' }}</h1>
        <button class="btn-back" (click)="goBack()">← Indietro</button>
      </div>

      <div class="loading" *ngIf="loading()">Caricamento...</div>
      <div class="error" *ngIf="error()">{{ error() }}</div>

      <form [formGroup]="taskForm" (ngSubmit)="onSubmit()" *ngIf="!loading()">
        <div class="form-group">
          <label for="projectId">Progetto *</label>
          <select id="projectId" formControlName="projectId" class="form-control">
            <option value="">-- Seleziona progetto --</option>
            <option *ngFor="let project of projects()" [value]="project.id">
              {{ project.name }}
            </option>
          </select>
          <div class="error-message" *ngIf="taskForm.get('projectId')?.invalid && taskForm.get('projectId')?.touched">
            Il progetto è obbligatorio
          </div>
        </div>

        <div class="form-group">
          <label for="title">Titolo *</label>
          <input
            id="title"
            type="text"
            formControlName="title"
            class="form-control"
            placeholder="Inserisci il titolo del task"
            maxlength="255"
          />
          <div class="error-message" *ngIf="taskForm.get('title')?.invalid && taskForm.get('title')?.touched">
            Il titolo è obbligatorio (max 255 caratteri)
          </div>
        </div>

        <div class="form-group">
          <label for="tag">Tag</label>
          <input
            id="tag"
            type="text"
            formControlName="tag"
            class="form-control"
            placeholder="es: Backend, Frontend, Bug, Feature"
            maxlength="100"
          />
          <small class="form-text">Categoria o etichetta per organizzare i task</small>
        </div>

        <div class="form-group">
          <label for="status">Stato *</label>
          <select id="status" formControlName="status" class="form-control">
            <option *ngFor="let status of taskStatuses" [value]="status">
              {{ getStatusLabel(status) }}
            </option>
          </select>
        </div>

        <div class="form-group">
          <label for="description">Descrizione</label>
          <textarea
            id="description"
            formControlName="description"
            class="form-control"
            rows="6"
            placeholder="Descrizione dettagliata del task..."
          ></textarea>
        </div>

        <div class="form-actions">
          <button type="button" class="btn-cancel" (click)="goBack()">Annulla</button>
          <button type="submit" class="btn-submit" [disabled]="taskForm.invalid || submitting()">
            {{ submitting() ? 'Salvataggio...' : (isEditMode ? 'Aggiorna' : 'Crea') }}
          </button>
        </div>
      </form>
    </div>
  `,
  styles: [`
    .task-form-container {
      padding: 20px;
      max-width: 800px;
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

    .btn-back {
      background: #ecf0f1;
      color: #2c3e50;
      border: none;
      padding: 10px 20px;
      border-radius: 6px;
      cursor: pointer;
      font-size: 0.95rem;
      transition: background 0.3s;
    }

    .btn-back:hover {
      background: #bdc3c7;
    }

    .loading, .error {
      text-align: center;
      padding: 40px;
      font-size: 1.2rem;
    }

    .error {
      color: #e74c3c;
    }

    form {
      background: white;
      padding: 30px;
      border-radius: 8px;
      box-shadow: 0 2px 8px rgba(0,0,0,0.1);
    }

    .form-group {
      margin-bottom: 24px;
    }

    label {
      display: block;
      margin-bottom: 8px;
      font-weight: 600;
      color: #2c3e50;
    }

    .form-control {
      width: 100%;
      padding: 10px 12px;
      border: 1px solid #ddd;
      border-radius: 4px;
      font-size: 1rem;
      transition: border-color 0.3s;
    }

    .form-control:focus {
      outline: none;
      border-color: #3498db;
    }

    textarea.form-control {
      resize: vertical;
      font-family: inherit;
    }

    .form-text {
      display: block;
      margin-top: 4px;
      color: #7f8c8d;
      font-size: 0.85rem;
    }

    .error-message {
      color: #e74c3c;
      font-size: 0.85rem;
      margin-top: 4px;
    }

    .form-actions {
      display: flex;
      gap: 12px;
      justify-content: flex-end;
      margin-top: 32px;
      padding-top: 24px;
      border-top: 1px solid #ecf0f1;
    }

    .btn-cancel, .btn-submit {
      padding: 12px 32px;
      border: none;
      border-radius: 6px;
      cursor: pointer;
      font-size: 1rem;
      font-weight: 600;
      transition: all 0.3s;
    }

    .btn-cancel {
      background: #ecf0f1;
      color: #2c3e50;
    }

    .btn-cancel:hover {
      background: #bdc3c7;
    }

    .btn-submit {
      background: #3498db;
      color: white;
    }

    .btn-submit:hover:not(:disabled) {
      background: #2980b9;
    }

    .btn-submit:disabled {
      background: #bdc3c7;
      cursor: not-allowed;
    }
  `]
})
export class TaskFormComponent implements OnInit {
  private fb = inject(FormBuilder);
  private taskService = inject(TaskService);
  private projectService = inject(ProjectService);
  private router = inject(Router);
  private route = inject(ActivatedRoute);

  taskForm!: FormGroup;
  projects = signal<Project[]>([]);
  loading = signal(true);
  submitting = signal(false);
  error = signal<string | null>(null);

  isEditMode = false;
  taskId?: number;

  taskStatuses: TaskStatus[] = [
    TaskStatus.TODO,
    TaskStatus.IN_PROGRESS,
    TaskStatus.COMPLETED,
    TaskStatus.BLOCKED,
    TaskStatus.CANCELLED
  ];

  ngOnInit(): void {
    this.initForm();
    this.loadProjects();

    // Check if edit mode
    const id = this.route.snapshot.paramMap.get('id');
    if (id) {
      this.isEditMode = true;
      this.taskId = +id;
      this.loadTask();
    } else {
      this.loading.set(false);
    }
  }

  initForm(): void {
    this.taskForm = this.fb.group({
      projectId: ['', Validators.required],
      title: ['', [Validators.required, Validators.maxLength(255)]],
      tag: ['', Validators.maxLength(100)],
      description: [''],
      status: [TaskStatus.TODO, Validators.required]
    });
  }

  loadProjects(): void {
    this.projectService.getAll().subscribe({
      next: (data) => {
        this.projects.set(data);
      },
      error: (err) => {
        this.error.set('Impossibile caricare i progetti.');
      }
    });
  }

  loadTask(): void {
    if (!this.taskId) return;

    this.taskService.getById(this.taskId).subscribe({
      next: (task) => {
        this.taskForm.patchValue({
          projectId: task.projectId,
          title: task.title,
          tag: task.tag || '',
          description: task.description || '',
          status: task.status
        });
        this.loading.set(false);
      },
      error: (err) => {
        this.error.set('Impossibile caricare il task.');
        this.loading.set(false);
      }
    });
  }

  onSubmit(): void {
    if (this.taskForm.invalid) return;

    this.submitting.set(true);

    const request: TaskRequest = {
      projectId: +this.taskForm.value.projectId,
      title: this.taskForm.value.title,
      tag: this.taskForm.value.tag || undefined,
      description: this.taskForm.value.description || undefined,
      status: this.taskForm.value.status
    };

    const operation = this.isEditMode && this.taskId
      ? this.taskService.update(this.taskId, request)
      : this.taskService.create(request);

    operation.subscribe({
      next: () => {
        this.submitting.set(false);
        this.goBack();
      },
      error: (err) => {
        this.submitting.set(false);
        alert('Errore durante il salvataggio del task.');
      }
    });
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

  goBack(): void {
    this.router.navigate(['/tasks']);
  }
}
