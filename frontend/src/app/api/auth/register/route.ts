import { NextRequest } from 'next/server';

export async function POST(request: NextRequest) {
  try {
    const userData = await request.json();

    // In a real application, you would:
    // 1. Validate the user data
    // 2. Hash the password
    // 3. Save the user to your database
    // 4. Generate a JWT token
    // 5. Return the token

    // For now, we'll simulate the registration process
    if (userData.email && userData.password && userData.name) {
      // Simulate API call
      await new Promise(resolve => setTimeout(resolve, 1000));

      // Create a mock token (in a real app, this would be a proper JWT)
      const mockToken = `mock-token-${Date.now()}-${Math.random().toString(36).substring(2)}`;

      return new Response(
        JSON.stringify({
          accessToken: mockToken,
          tokenType: 'Bearer',
          user: {
            id: `user-${Date.now()}`,
            email: userData.email,
            name: userData.name,
            role: 'student',
            backgroundSoftware: userData.backgroundSoftware || '',
            backgroundHardware: userData.backgroundHardware || ''
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
          error: 'Email, password, and name are required',
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
    console.error('Error during registration:', error);
    return new Response(
      JSON.stringify({
        error: 'Failed to process registration request. Please try again later.',
        details: error instanceof Error ? error.message : String(error)
      }),
      {
        status: 500,
        headers: { 'Content-Type': 'application/json' }
      }
    );
  }
}