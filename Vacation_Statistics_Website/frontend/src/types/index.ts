// Type definitions for the application

export interface User {
    email: string;
    first_name: string;
    last_name: string;
  }
  
  export interface LoginCredentials {
    email: string;
    password: string;
  }
  
  export interface AuthResponse {
    access_token: string;
    user: User;
  }
  
  export interface VacationStats {
    pastVacations: number;
    ongoingVacations: number;
    futureVacations: number;
  }
  
  export interface TotalUsers {
    totalUsers: number;
  }
  
  export interface TotalLikes {
    totalLikes: number;
  }
  
  export interface LikeDistribution {
    destination: string;
    likes: number;
  }
  
  export interface SummaryStats {
    vacationStats: VacationStats;
    totalUsers: number;
    totalLikes: number;
    topDestinations: LikeDistribution[];
  }
  
  export interface AuthContextType {
    user: User | null;
    token: string | null;
    login: (credentials: LoginCredentials) => Promise<void>;
    logout: () => void;
    isAuthenticated: boolean;
    isLoading: boolean;
  }