// Enums che corrispondono al backend Java

export enum ProjectType {
  FREELANCE = 'FREELANCE',
  VACATION_RENTAL = 'VACATION_RENTAL',
  SAAS = 'SAAS'
}

export enum ProjectStatus {
  ACTIVE = 'ACTIVE',
  ARCHIVED = 'ARCHIVED',
  SUSPENDED = 'SUSPENDED'
}

export enum CostCategory {
  INFRASTRUCTURE = 'INFRASTRUCTURE',
  BRANDING = 'BRANDING',
  CONTENT = 'CONTENT',
  DEVELOPMENT = 'DEVELOPMENT',
  MARKETING = 'MARKETING',
  PROPERTY = 'PROPERTY',
  TOOLS = 'TOOLS',
  OTHER = 'OTHER'
}

export enum PaymentStatus {
  PENDING = 'PENDING',
  PAID = 'PAID',
  RECEIVED = 'RECEIVED',
  CANCELLED = 'CANCELLED'
}

export enum Frequency {
  MONTHLY = 'MONTHLY',
  QUARTERLY = 'QUARTERLY',
  YEARLY = 'YEARLY'
}

export enum RevenueType {
  CONSULTATION = 'CONSULTATION',
  PROJECT = 'PROJECT',
  COURSE = 'COURSE',
  PASSIVE = 'PASSIVE',
  BOOKING = 'BOOKING',
  SUBSCRIPTION = 'SUBSCRIPTION',
  OTHER = 'OTHER'
}

export enum BookingStatus {
  PENDING = 'PENDING',
  CONFIRMED = 'CONFIRMED',
  CANCELLED = 'CANCELLED',
  COMPLETED = 'COMPLETED'
}

export enum SubscriptionStatus {
  ACTIVE = 'ACTIVE',
  TRIAL = 'TRIAL',
  CANCELLED = 'CANCELLED',
  EXPIRED = 'EXPIRED'
}

export enum BillingCycle {
  MONTHLY = 'MONTHLY',
  YEARLY = 'YEARLY'
}

export enum MetricType {
  ROI = 'ROI',
  PROFIT = 'PROFIT',
  OCCUPANCY_RATE = 'OCCUPANCY_RATE',
  ADR = 'ADR',
  REVPAR = 'REVPAR',
  MRR = 'MRR',
  ARR = 'ARR',
  CHURN_RATE = 'CHURN_RATE',
  CAC = 'CAC',
  LTV = 'LTV'
}

export enum PeriodType {
  DAILY = 'DAILY',
  WEEKLY = 'WEEKLY',
  MONTHLY = 'MONTHLY',
  QUARTERLY = 'QUARTERLY',
  YEARLY = 'YEARLY'
}

export enum TaskStatus {
  TODO = 'TODO',
  IN_PROGRESS = 'IN_PROGRESS',
  COMPLETED = 'COMPLETED',
  BLOCKED = 'BLOCKED',
  CANCELLED = 'CANCELLED'
}
