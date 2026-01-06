import { Injectable, inject } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { environment } from '../../../environments/environment';
import { Project, ProjectCreateRequest, ProjectStatus, ProjectType } from '../models';

@Injectable({
  providedIn: 'root'
})
export class ProjectService {
  private http = inject(HttpClient);
  private apiUrl = `${environment.apiUrl}/projects`;

  getAll(): Observable<Project[]> {
    return this.http.get<Project[]>(this.apiUrl);
  }

  getById(id: number): Observable<Project> {
    return this.http.get<Project>(`${this.apiUrl}/${id}`);
  }

  getByCode(code: string): Observable<Project> {
    return this.http.get<Project>(`${this.apiUrl}/code/${code}`);
  }

  getByStatus(status: ProjectStatus): Observable<Project[]> {
    return this.http.get<Project[]>(`${this.apiUrl}/status/${status}`);
  }

  getByType(type: ProjectType): Observable<Project[]> {
    return this.http.get<Project[]>(`${this.apiUrl}/type/${type}`);
  }

  create(request: ProjectCreateRequest): Observable<Project> {
    return this.http.post<Project>(this.apiUrl, request);
  }

  update(id: number, request: ProjectCreateRequest): Observable<Project> {
    return this.http.put<Project>(`${this.apiUrl}/${id}`, request);
  }

  delete(id: number): Observable<void> {
    return this.http.delete<void>(`${this.apiUrl}/${id}`);
  }

  archive(id: number): Observable<Project> {
    return this.http.patch<Project>(`${this.apiUrl}/${id}/archive`, {});
  }

  changeStatus(id: number, status: ProjectStatus): Observable<Project> {
    return this.http.patch<Project>(`${this.apiUrl}/${id}/status/${status}`, {});
  }
}
