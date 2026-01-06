import { Injectable, inject } from '@angular/core';
import { HttpClient, HttpParams } from '@angular/common/http';
import { Observable } from 'rxjs';
import { environment } from '../../../environments/environment';
import { Task, TaskRequest } from '../models/task.model';
import { TaskStatus } from '../models/enums';

/**
 * Service for managing tasks via REST API
 */
@Injectable({
  providedIn: 'root'
})
export class TaskService {
  private http = inject(HttpClient);
  private apiUrl = `${environment.apiUrl}/tasks`;

  /**
   * Get all tasks
   */
  getAll(): Observable<Task[]> {
    return this.http.get<Task[]>(this.apiUrl);
  }

  /**
   * Get task by ID
   */
  getById(id: number): Observable<Task> {
    return this.http.get<Task>(`${this.apiUrl}/${id}`);
  }

  /**
   * Get all tasks for a specific project
   */
  getByProjectId(projectId: number): Observable<Task[]> {
    return this.http.get<Task[]>(`${this.apiUrl}/project/${projectId}`);
  }

  /**
   * Get tasks by project and status
   */
  getByProjectIdAndStatus(projectId: number, status: TaskStatus): Observable<Task[]> {
    return this.http.get<Task[]>(`${this.apiUrl}/project/${projectId}/status/${status}`);
  }

  /**
   * Get tasks by project and tag
   */
  getByProjectIdAndTag(projectId: number, tag: string): Observable<Task[]> {
    return this.http.get<Task[]>(`${this.apiUrl}/project/${projectId}/tag/${tag}`);
  }

  /**
   * Get all tasks with a specific status
   */
  getByStatus(status: TaskStatus): Observable<Task[]> {
    return this.http.get<Task[]>(`${this.apiUrl}/status/${status}`);
  }

  /**
   * Get all distinct tags for a project
   */
  getDistinctTags(projectId: number): Observable<string[]> {
    return this.http.get<string[]>(`${this.apiUrl}/project/${projectId}/tags`);
  }

  /**
   * Count tasks by project and status
   */
  countByProjectIdAndStatus(projectId: number, status: TaskStatus): Observable<number> {
    return this.http.get<number>(`${this.apiUrl}/project/${projectId}/status/${status}/count`);
  }

  /**
   * Count total tasks for a project
   */
  countByProjectId(projectId: number): Observable<number> {
    return this.http.get<number>(`${this.apiUrl}/project/${projectId}/count`);
  }

  /**
   * Create a new task
   */
  create(request: TaskRequest): Observable<Task> {
    return this.http.post<Task>(this.apiUrl, request);
  }

  /**
   * Update an existing task
   */
  update(id: number, request: TaskRequest): Observable<Task> {
    return this.http.put<Task>(`${this.apiUrl}/${id}`, request);
  }

  /**
   * Delete a task
   */
  delete(id: number): Observable<void> {
    return this.http.delete<void>(`${this.apiUrl}/${id}`);
  }
}
