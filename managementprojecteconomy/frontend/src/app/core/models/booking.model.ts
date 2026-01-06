import { BookingStatus } from './enums';

export interface Booking {
  id: number;
  projectId: number;
  projectName: string;
  checkinDate: string;
  checkoutDate: string;
  guests: number;
  nights: number;
  price: number;
  pricePerNight: number;
  platform: string;
  commissionRate: number;
  commissionAmount: number;
  netRevenue: number;
  bookingStatus: BookingStatus;
  guestName?: string;
  guestEmail?: string;
  guestPhone?: string;
  createdAt: string;
  updatedAt: string;
}

export interface BookingCreateRequest {
  projectId: number;
  checkinDate: string;
  checkoutDate: string;
  guests: number;
  price: number;
  platform: string;
  bookingStatus?: BookingStatus;
  guestName?: string;
  guestEmail?: string;
  guestPhone?: string;
}
