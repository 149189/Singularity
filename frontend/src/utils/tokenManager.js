// frontend/src/utils/tokenManager.js
class TokenManager {
  constructor() {
    this.ACCESS_TOKEN_KEY = "access_token";
    this.REFRESH_TOKEN_KEY = "refresh_token";
    this.TOKEN_EXPIRY_KEY = "token_expiry";
  }

  setTokens(accessToken, refreshToken) {
    // Store in httpOnly cookies in production
    sessionStorage.setItem(this.ACCESS_TOKEN_KEY, accessToken);
    localStorage.setItem(this.REFRESH_TOKEN_KEY, refreshToken);

    // Set expiry time (30 minutes from now)
    const expiryTime = Date.now() + 30 * 60 * 1000;
    localStorage.setItem(this.TOKEN_EXPIRY_KEY, expiryTime.toString());
  }

  getAccessToken() {
    return sessionStorage.getItem(this.ACCESS_TOKEN_KEY);
  }

  getRefreshToken() {
    return localStorage.getItem(this.REFRESH_TOKEN_KEY);
  }

  isTokenExpired() {
    const expiryTime = localStorage.getItem(this.TOKEN_EXPIRY_KEY);
    if (!expiryTime) return true;

    return Date.now() > parseInt(expiryTime);
  }

  clearTokens() {
    sessionStorage.removeItem(this.ACCESS_TOKEN_KEY);
    localStorage.removeItem(this.REFRESH_TOKEN_KEY);
    localStorage.removeItem(this.TOKEN_EXPIRY_KEY);
  }
}

export const tokenManager = new TokenManager();
