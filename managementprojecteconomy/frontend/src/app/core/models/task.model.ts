import { TaskStatus } from './enums';

/**
 * Task model interface
 */
export interface Task {
  id: number;
  projectId: number;
  projectName: string;
  title: string;
  tag?: string;
  description?: string;
  status: TaskStatus;
  createdAt: string;
  updatedAt: string;
}

/**
 * Task creation/update request interface
 */
export interface TaskRequest {
  projectId: number;
  title: string;
  tag?: string;
  description?: string;
  status: TaskStatus;
}
