import Link from 'next/link';

export default function Home() {
  return (
    <div className="min-h-screen bg-gradient-to-b from-blue-50 to-white">
      {/* Header */}
      <header className="bg-white shadow-sm">
        <div className="container mx-auto px-4 py-4 flex justify-between items-center">
          <h1 className="text-2xl font-bold text-blue-600">Physical AI & Humanoid Robotics</h1>
          <nav>
            <ul className="flex space-x-6">
              <li><Link href="/login" className="text-blue-600 hover:underline">Login</Link></li>
              <li><Link href="/register" className="text-blue-600 hover:underline">Register</Link></li>
            </ul>
          </nav>
        </div>
      </header>

      {/* Hero Section */}
      <main className="container mx-auto px-4 py-16">
        <div className="max-w-3xl mx-auto text-center">
          <h1 className="text-4xl md:text-5xl font-bold text-gray-900 mb-6">
            Learn Physical AI & Humanoid Robotics
          </h1>
          <p className="text-xl text-gray-600 mb-10">
            An interactive textbook platform with AI-powered assistance, personalized learning, and multilingual support
          </p>

          <div className="flex flex-col sm:flex-row justify-center gap-4">
            <Link
              href="/book"
              className="inline-block px-6 py-3 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors"
            >
              Start Learning
            </Link>
            <Link
              href="/chat"
              className="inline-block px-6 py-3 bg-white text-blue-600 border border-blue-600 rounded-lg hover:bg-blue-50 transition-colors"
            >
              Try AI Assistant
            </Link>
          </div>
        </div>

        {/* Features */}
        <div className="mt-20 grid grid-cols-1 md:grid-cols-3 gap-8">
          <div className="bg-white p-6 rounded-lg shadow-md">
            <h3 className="text-xl font-semibold mb-3">AI-Powered Learning</h3>
            <p className="text-gray-600">
              Get instant answers to your questions with our RAG chatbot powered by OpenAI
            </p>
          </div>
          <div className="bg-white p-6 rounded-lg shadow-md">
            <h3 className="text-xl font-semibold mb-3">Personalized Content</h3>
            <p className="text-gray-600">
              Content adapted to your software and hardware background for optimal learning
            </p>
          </div>
          <div className="bg-white p-6 rounded-lg shadow-md">
            <h3 className="text-xl font-semibold mb-3">Multilingual Support</h3>
            <p className="text-gray-600">
              Learn in Urdu with our AI-powered translation feature
            </p>
          </div>
        </div>
      </main>

      {/* Footer */}
      <footer className="bg-gray-100 py-8 mt-16">
        <div className="container mx-auto px-4 text-center text-gray-600">
          <p>© {new Date().getFullYear()} Physical AI & Humanoid Robotics Textbook Platform. All rights reserved.</p>
        </div>
      </footer>
    </div>
  );
}