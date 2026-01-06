import { RevenueType, PaymentStatus } from './enums';

export interface RevenueStream {
  id: number;
  projectId: number;
  projectName: string;
  name: string;
  amount: number;
  revenueDate: string;
  source?: string;
  revenueType: RevenueType;
  description?: string;
  invoiceNumber?: string;
  paymentStatus: PaymentStatus;
  createdAt: string;
  updatedAt: string;
}

export interface RevenueStreamRequest {
  projectId: number;
  name: string;
  amount: number;
  revenueDate: string;
  source?: string;
  revenueType: RevenueType;
  description?: string;
  invoiceNumber?: string;
  paymentStatus?: PaymentStatus;
}
