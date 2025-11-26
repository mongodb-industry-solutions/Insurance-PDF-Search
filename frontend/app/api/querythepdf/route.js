export async function POST(request) {
  const body = await request.json();
  
  // Use the environment variable for the backend URL
  const backendUrl = process.env.NEXT_PUBLIC_ASK_THE_PDF_API_URL;

  if (!backendUrl) {
    return Response.json(
      { error: 'Backend URL not configured', details: 'NEXT_PUBLIC_ASK_THE_PDF_API_URL environment variable is missing' },
      { status: 500 }
    );
  }

  try {
    const response = await fetch(`${backendUrl}/querythepdf`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(body),
    });

    if (!response.ok) {
      const error = await response.json().catch(() => ({ detail: 'Request failed' }));
      return Response.json(error, { status: response.status});
    }

    const data = await response.json();
    return Response.json(data);
  } catch (error) {
    return Response.json(
      { error: 'Failed to connect to backend', details: error.message },
      { status: 500 }
    );
  }
}