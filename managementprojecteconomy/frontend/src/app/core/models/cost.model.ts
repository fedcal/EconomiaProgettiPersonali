import { CostCategory, PaymentStatus, Frequency } from './enums';

export interface OneTimeCost {
  id: number;
  projectId: number;
  projectName: string;
  name: string;
  amount: number;
  costDate: string;
  category: CostCategory;
  description?: string;
  invoiceNumber?: string;
  supplier?: string;
  paymentStatus: PaymentStatus;
  createdAt: string;
  updatedAt: string;
}

export interface OneTimeCostRequest {
  projectId: number;
  name: string;
  amount: number;
  costDate: string;
  category: CostCategory;
  description?: string;
  invoiceNumber?: string;
  supplier?: string;
  paymentStatus?: PaymentStatus;
}

export interface RecurringCost {
  id: number;
  projectId: number;
  projectName: string;
  name: string;
  amount: number;
  frequency: Frequency;
  category: CostCategory;
  startDate: string;
  endDate?: string;
  description?: string;
  isActive: boolean;
  autoRenew: boolean;
  createdAt: string;
  updatedAt: string;
}

export interface RecurringCostRequest {
  projectId: number;
  name: string;
  amount: number;
  frequency: Frequency;
  category: CostCategory;
  startDate: string;
  endDate?: string;
  description?: string;
  isActive?: boolean;
  autoRenew?: boolean;
}
