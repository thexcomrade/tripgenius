import axios, { AxiosError, AxiosInstance } from "axios";

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL ?? "http://127.0.0.1:8000";

export interface RegisterRequest {
  full_name: string;
  email: string;
  password: string;
}

export interface LoginRequest {
  email: string;
  password: string;
}

export interface RegisterResponse {
  message: string;
  user_id: string;
  email: string;
}

export interface LoginResponse {
  message: string;
  access_token: string;
  token_type: string;
}

export interface CurrentUser {
  id: string;
  full_name: string;
  email: string;
  is_active: boolean;
  is_verified: boolean;
  eco_travel_score: number;
  total_trips: number;
  created_at: string;
}

export interface ChangePasswordRequest {
  current_password: string;
  new_password: string;
}

class AuthService {
  private readonly api: AxiosInstance;

  constructor() {
    this.api = axios.create({
      baseURL: API_BASE_URL,
      timeout: 30000,
      headers: {
        "Content-Type": "application/json",
      },
    });

    this.api.interceptors.request.use((config) => {
      const token = this.getAccessToken();

      if (token && config.headers) {
        config.headers.Authorization = `Bearer ${token}`;
      }

      return config;
    });
  }

  async register(payload: RegisterRequest): Promise<RegisterResponse> {
    try {
      const response = await this.api.post<RegisterResponse>(
        "/api/auth/register",
        payload,
      );

      return response.data;
    } catch (error) {
      throw this.handleError(error);
    }
  }

  async login(payload: LoginRequest): Promise<LoginResponse> {
    try {
      const response = await this.api.post<LoginResponse>(
        "/api/auth/login",
        payload,
      );

      const data = response.data;

      this.setAccessToken(data.access_token);

      return data;
    } catch (error) {
      throw this.handleError(error);
    }
  }

  async getProfile(): Promise<CurrentUser> {
    try {
      const response = await this.api.get<CurrentUser>("/api/auth/profile");

      return response.data;
    } catch (error) {
      throw this.handleError(error);
    }
  }

  async changePassword(payload: ChangePasswordRequest): Promise<void> {
    try {
      await this.api.post("/api/auth/change-password", payload);
    } catch (error) {
      throw this.handleError(error);
    }
  }

  async getStatus(): Promise<any> {
    try {
      const response = await this.api.get("/api/auth/status");

      return response.data;
    } catch (error) {
      throw this.handleError(error);
    }
  }

  async logout(): Promise<void> {
    try {
      await this.api.post("/api/auth/logout");
    } catch {
      // Ignore backend logout errors
    }

    this.removeAccessToken();
  }

  setAccessToken(token: string): void {
    if (typeof window !== "undefined") {
      localStorage.setItem("tripgenius_token", token);
    }
  }

  getAccessToken(): string | null {
    if (typeof window === "undefined") {
      return null;
    }

    return localStorage.getItem("tripgenius_token");
  }

  removeAccessToken(): void {
    if (typeof window !== "undefined") {
      localStorage.removeItem("tripgenius_token");
    }
  }

  isAuthenticated(): boolean {
    return !!this.getAccessToken();
  }

  private handleError(error: unknown): Error {
    if (axios.isAxiosError(error)) {
      const axiosError = error as AxiosError<any>;

      const message =
        axiosError.response?.data?.detail ||
        axiosError.response?.data?.message ||
        axiosError.message ||
        "Request failed";

      return new Error(message);
    }

    return new Error("Unexpected error occurred");
  }
}

export const authService = new AuthService();

export default authService;
