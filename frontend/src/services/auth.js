export const checkAuth = async () => {
  try {
    const response = await fetch(`${process.env.REACT_APP_API_URL || 'http://localhost:8000'}/accounts/profile/`, {
      credentials: 'include'
    });
    return response.ok;
  } catch (error) {
    console.error('Auth check failed:', error);
    return false;
  }
};

export const login = async (username, password) => {
  try {
    const response = await fetch(`${process.env.REACT_APP_API_URL || 'http://localhost:8000'}/accounts/login/`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      credentials: 'include',
      body: JSON.stringify({ username, password })
    });
    
    return response.ok;
  } catch (error) {
    console.error('Login failed:', error);
    return false;
  }
};

export const logout = async () => {
  try {
    await fetch(`${process.env.REACT_APP_API_URL || 'http://localhost:8000'}/accounts/logout/`, {
      method: 'POST',
      credentials: 'include'
    });
    return true;
  } catch (error) {
    console.error('Logout failed:', error);
    return false;
  }
};
