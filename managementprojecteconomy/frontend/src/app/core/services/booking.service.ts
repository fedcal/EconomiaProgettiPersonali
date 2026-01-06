import { Injectable, inject } from '@angular/core';
import { HttpClient, HttpParams } from '@angular/common/http';
import { Observable } from 'rxjs';
import { environment } from '../../../environments/environment';
import { Booking, BookingCreateRequest } from '../models';

@Injectable({
  providedIn: 'root'
})
export class BookingService {
  private http = inject(HttpClient);
  private apiUrl = `${environment.apiUrl}/bookings`;

  getAll(): Observable<Booking[]> {
    return this.http.get<Booking[]>(this.apiUrl);
  }

  getById(id: number): Observable<Booking> {
    return this.http.get<Booking>(`${this.apiUrl}/${id}`);
  }

  getByProject(projectId: number): Observable<Booking[]> {
    return this.http.get<Booking[]>(`${this.apiUrl}/project/${projectId}`);
  }

  getByDateRange(projectId: number, startDate: string, endDate: string): Observable<Booking[]> {
    const params = new HttpParams()
      .set('startDate', startDate)
      .set('endDate', endDate);

    return this.http.get<Booking[]>(`${this.apiUrl}/project/${projectId}/date-range`, { params });
  }

  getByYear(projectId: number, year: number): Observable<Booking[]> {
    return this.http.get<Booking[]>(`${this.apiUrl}/project/${projectId}/year/${year}`);
  }

  getByPlatform(projectId: number, platform: string): Observable<Booking[]> {
    return this.http.get<Booking[]>(`${this.apiUrl}/project/${projectId}/platform/${platform}`);
  }

  create(request: BookingCreateRequest): Observable<Booking> {
    return this.http.post<Booking>(this.apiUrl, request);
  }

  update(id: number, request: BookingCreateRequest): Observable<Booking> {
    return this.http.put<Booking>(`${this.apiUrl}/${id}`, request);
  }

  delete(id: number): Observable<void> {
    return this.http.delete<void>(`${this.apiUrl}/${id}`);
  }

  cancel(id: number): Observable<Booking> {
    return this.http.patch<Booking>(`${this.apiUrl}/${id}/cancel`, {});
  }

  calculateADR(projectId: number, year: number): Observable<{ adr: number }> {
    return this.http.get<{ adr: number }>(`${this.apiUrl}/project/${projectId}/adr/${year}`);
  }

  calculateOccupancyRate(projectId: number, year: number): Observable<{ occupancyRate: number }> {
    return this.http.get<{ occupancyRate: number }>(`${this.apiUrl}/project/${projectId}/occupancy-rate/${year}`);
  }
}
