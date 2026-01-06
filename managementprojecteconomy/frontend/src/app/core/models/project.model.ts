import { ProjectType, ProjectStatus } from './enums';

export interface Project {
  id: number;
  name: string;
  code: string;
  type: ProjectType;
  startDate: string;
  currency: string;
  status: ProjectStatus;
  targetOccupancyRate?: number;
  targetMonthlyRevenue?: number;
  targetRoi?: number;
  createdAt: string;
  updatedAt: string;
}

export interface ProjectCreateRequest {
  name: string;
  code: string;
  type: ProjectType;
  startDate: string;
  currency?: string;
  status?: ProjectStatus;
  targetOccupancyRate?: number;
  targetMonthlyRevenue?: number;
  targetRoi?: number;
}
