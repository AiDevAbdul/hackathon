import { NextRequest } from 'next/server';

export async function POST(request: NextRequest) {
  try {
    const { email, password } = await request.json();

    // In a real application, you would:
    // 1. Validate the credentials against your backend
    // 2. Generate a JWT token
    // 3. Return the token

    // For now, we'll simulate the login process
    if (email && password) {
      // Simulate API call
      await new Promise(resolve => setTimeout(resolve, 1000));

      // Create a mock token (in a real app, this would be a proper JWT)
      const mockToken = `mock-token-${Date.now()}-${Math.random().toString(36).substring(2)}`;

      return new Response(
        JSON.stringify({
          accessToken: mockToken,
          tokenType: 'Bearer',
          user: {
            id: 'user-123',
            email,
            name: email.split('@')[0],
            role: 'student',
            backgroundSoftware: 'Software Developer',
            backgroundHardware: 'Robotics Enthusiast'
          }
        }),
        {
          status: 200,
          headers: {
            'Content-Type': 'application/json',
          },
        }
      );
    } else {
      return new Response(
        JSON.stringify({
          error: 'Email and password are required',
        }),
        {
          status: 400,
          headers: {
            'Content-Type': 'application/json',
          },
        }
      );
    }
  } catch (error) {
    console.error('Error during login:', error);
    return new Response(
      JSON.stringify({
        error: 'Failed to process login request. Please try again later.',
        details: error instanceof Error ? error.message : String(error)
      }),
      {
        status: 500,
        headers: { 'Content-Type': 'application/json' }
      }
    );
  }
}