import { Component, OnInit, signal, inject } from '@angular/core';
import { CommonModule } from '@angular/common';
import { Router, RouterModule } from '@angular/router';
import { ProjectService } from '../../core/services/project.service';
import { Project, ProjectType } from '../../core/models';

@Component({
  selector: 'app-dashboard',
  standalone: true,
  imports: [CommonModule, RouterModule],
  template: `
    <div class="dashboard-container">
      <header class="dashboard-header">
        <div class="header-content">
          <div>
            <h1>Management Project Economy</h1>
            <p>Sistema di gestione economica multi-progetto</p>
          </div>
          <nav class="main-nav">
            <a routerLink="/dashboard" routerLinkActive="active" class="nav-link">📊 Dashboard</a>
            <a routerLink="/tasks" routerLinkActive="active" class="nav-link">✅ Task</a>
          </nav>
        </div>
      </header>

      <div class="loading" *ngIf="loading()">
        <p>Caricamento progetti in corso...</p>
      </div>

      <div class="error" *ngIf="error()">
        <p>⚠️ {{ error() }}</p>
        <button (click)="loadProjects()">Riprova</button>
      </div>

      <div class="projects-grid" *ngIf="!loading() && !error()">
        <div class="project-card" *ngFor="let project of projects()">
          <div class="project-header">
            <h2>{{ project.name }}</h2>
            <span class="project-type" [class]="'type-' + project.type.toLowerCase()">
              {{ getProjectTypeLabel(project.type) }}
            </span>
          </div>

          <div class="project-info">
            <div class="info-row">
              <span class="label">Codice:</span>
              <span class="value">{{ project.code }}</span>
            </div>
            <div class="info-row">
              <span class="label">Stato:</span>
              <span class="status" [class]="'status-' + project.status.toLowerCase()">
                {{ project.status }}
              </span>
            </div>
            <div class="info-row">
              <span class="label">Data Inizio:</span>
              <span class="value">{{ project.startDate | date:'dd/MM/yyyy' }}</span>
            </div>
            <div class="info-row" *ngIf="project.targetMonthlyRevenue">
              <span class="label">Target Mensile:</span>
              <span class="value">{{ project.targetMonthlyRevenue | currency:'EUR' }}</span>
            </div>
          </div>

          <div class="project-actions">
            <button class="btn btn-primary">Visualizza Dettagli</button>
            <button class="btn btn-secondary">Analytics</button>
          </div>
        </div>

        <div class="empty-state" *ngIf="projects().length === 0">
          <p>Nessun progetto trovato</p>
          <button class="btn btn-primary">+ Aggiungi Progetto</button>
        </div>
      </div>

      <footer class="dashboard-footer">
        <p>
          Backend API: <span class="api-status">{{ apiUrl }}</span>
        </p>
        <p>Versione 1.0.0 - © 2026 Federico Calò</p>
      </footer>
    </div>
  `,
  styles: [`
    .dashboard-container {
      min-height: 100vh;
      background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
      padding: 2rem;
    }

    .dashboard-header {
      color: white;
      margin-bottom: 3rem;
    }

    .header-content {
      display: flex;
      justify-content: space-between;
      align-items: center;
      max-width: 1200px;
      margin: 0 auto;
    }

    .dashboard-header h1 {
      font-size: 2.5rem;
      margin-bottom: 0.5rem;
    }

    .dashboard-header p {
      font-size: 1.2rem;
      opacity: 0.9;
    }

    .main-nav {
      display: flex;
      gap: 1rem;
    }

    .nav-link {
      color: white;
      text-decoration: none;
      padding: 0.75rem 1.5rem;
      border-radius: 8px;
      font-weight: 600;
      transition: all 0.3s;
      background: rgba(255, 255, 255, 0.1);
    }

    .nav-link:hover {
      background: rgba(255, 255, 255, 0.2);
    }

    .nav-link.active {
      background: white;
      color: #667eea;
    }

    .loading, .error {
      background: white;
      padding: 2rem;
      border-radius: 8px;
      text-align: center;
      max-width: 600px;
      margin: 0 auto;
    }

    .error p {
      color: #e74c3c;
      margin-bottom: 1rem;
    }

    .projects-grid {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(350px, 1fr));
      gap: 2rem;
      max-width: 1200px;
      margin: 0 auto;
    }

    .project-card {
      background: white;
      border-radius: 12px;
      padding: 1.5rem;
      box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
      transition: transform 0.2s;
    }

    .project-card:hover {
      transform: translateY(-4px);
      box-shadow: 0 8px 12px rgba(0, 0, 0, 0.15);
    }

    .project-header {
      display: flex;
      justify-content: space-between;
      align-items: start;
      margin-bottom: 1.5rem;
      border-bottom: 2px solid #f0f0f0;
      padding-bottom: 1rem;
    }

    .project-header h2 {
      font-size: 1.5rem;
      color: #2c3e50;
      margin: 0;
    }

    .project-type {
      padding: 0.25rem 0.75rem;
      border-radius: 20px;
      font-size: 0.75rem;
      font-weight: bold;
      text-transform: uppercase;
    }

    .type-freelance {
      background: #3498db;
      color: white;
    }

    .type-vacation_rental {
      background: #2ecc71;
      color: white;
    }

    .type-saas {
      background: #9b59b6;
      color: white;
    }

    .project-info {
      margin-bottom: 1.5rem;
    }

    .info-row {
      display: flex;
      justify-content: space-between;
      padding: 0.5rem 0;
      border-bottom: 1px solid #f5f5f5;
    }

    .info-row .label {
      font-weight: 600;
      color: #7f8c8d;
    }

    .info-row .value {
      color: #2c3e50;
    }

    .status {
      padding: 0.25rem 0.5rem;
      border-radius: 4px;
      font-size: 0.85rem;
      font-weight: 600;
    }

    .status-active {
      background: #d4edda;
      color: #155724;
    }

    .status-archived {
      background: #d6d8db;
      color: #383d41;
    }

    .project-actions {
      display: flex;
      gap: 0.5rem;
    }

    .btn {
      flex: 1;
      padding: 0.75rem;
      border: none;
      border-radius: 6px;
      cursor: pointer;
      font-weight: 600;
      transition: all 0.2s;
    }

    .btn-primary {
      background: #667eea;
      color: white;
    }

    .btn-primary:hover {
      background: #5568d3;
    }

    .btn-secondary {
      background: #f8f9fa;
      color: #495057;
      border: 1px solid #dee2e6;
    }

    .btn-secondary:hover {
      background: #e9ecef;
    }

    .empty-state {
      grid-column: 1 / -1;
      text-align: center;
      padding: 4rem 2rem;
      background: white;
      border-radius: 12px;
    }

    .empty-state p {
      font-size: 1.2rem;
      color: #7f8c8d;
      margin-bottom: 1.5rem;
    }

    .dashboard-footer {
      text-align: center;
      color: white;
      margin-top: 3rem;
      opacity: 0.8;
    }

    .api-status {
      font-family: monospace;
      background: rgba(255, 255, 255, 0.2);
      padding: 0.25rem 0.5rem;
      border-radius: 4px;
    }
  `]
})
export class DashboardComponent implements OnInit {
  private projectService = inject(ProjectService);

  projects = signal<Project[]>([]);
  loading = signal(true);
  error = signal<string | null>(null);
  apiUrl = 'http://localhost:8083/api/v1';

  ngOnInit(): void {
    this.loadProjects();
  }

  loadProjects(): void {
    this.loading.set(true);
    this.error.set(null);

    this.projectService.getAll().subscribe({
      next: (data) => {
        this.projects.set(data);
        this.loading.set(false);
      },
      error: (err) => {
        console.error('Error loading projects:', err);
        this.error.set(
          'Impossibile caricare i progetti. Assicurati che il backend sia in esecuzione su ' + this.apiUrl
        );
        this.loading.set(false);
      }
    });
  }

  getProjectTypeLabel(type: ProjectType): string {
    const labels: Record<ProjectType, string> = {
      [ProjectType.FREELANCE]: 'Freelance',
      [ProjectType.VACATION_RENTAL]: 'Vacation Rental',
      [ProjectType.SAAS]: 'SaaS'
    };
    return labels[type] || type;
  }
}
