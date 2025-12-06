import Link from 'next/link';

export default function BookPage() {
  // This would typically fetch from your backend in a real implementation
  const textbookModules = [
    {
      id: 'module1',
      title: 'The Robotic Nervous System (ROS 2)',
      description: 'Learn about the Robot Operating System and how it enables communication between robotic components.',
      lessons: [
        { id: 'lesson1-1', title: 'Introduction to ROS 2' },
        { id: 'lesson1-2', title: 'Nodes and Topics' },
        { id: 'lesson1-3', title: 'Services and Actions' },
      ]
    },
    {
      id: 'module2',
      title: 'The Digital Twin (Gazebo & Unity)',
      description: 'Explore simulation environments for testing and validating robotic systems.',
      lessons: [
        { id: 'lesson2-1', title: 'Gazebo Simulation' },
        { id: 'lesson2-2', title: 'Unity Robotics' },
        { id: 'lesson2-3', title: 'Simulation Best Practices' },
      ]
    },
    {
      id: 'module3',
      title: 'The AI-Robot Brain (NVIDIA Isaac™)',
      description: 'Discover how AI and machine learning enable intelligent robotic behavior.',
      lessons: [
        { id: 'lesson3-1', title: 'NVIDIA Isaac SDK' },
        { id: 'lesson3-2', title: 'Perception Systems' },
        { id: 'lesson3-3', title: 'Planning and Control' },
      ]
    },
    {
      id: 'module4',
      title: 'Vision-Language-Action (VLA)',
      description: 'Understand how robots can perceive, understand, and interact with the world.',
      lessons: [
        { id: 'lesson4-1', title: 'Computer Vision Fundamentals' },
        { id: 'lesson4-2', title: 'Language Understanding' },
        { id: 'lesson4-3', title: 'Action Execution' },
      ]
    }
  ];

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <header className="bg-white shadow">
        <div className="max-w-7xl mx-auto px-4 py-6 sm:px-6 lg:px-8 flex justify-between items-center">
          <h1 className="text-2xl font-bold text-gray-900">Physical AI & Humanoid Robotics Textbook</h1>
          <div className="flex items-center space-x-4">
            <Link href="/chat" className="bg-blue-500 text-white px-4 py-2 rounded-lg hover:bg-blue-600">
              AI Assistant
            </Link>
          </div>
        </div>
      </header>

      <main className="max-w-7xl mx-auto px-4 py-6 sm:px-6 lg:px-8">
        <div className="mb-8">
          <h2 className="text-xl font-semibold text-gray-800 mb-4">Course Modules</h2>
          <p className="text-gray-600">
            Explore the comprehensive curriculum designed to teach Physical AI and Humanoid Robotics.
          </p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          {textbookModules.map((module) => (
            <div key={module.id} className="bg-white rounded-lg shadow-md overflow-hidden">
              <div className="p-6">
                <h3 className="text-lg font-semibold text-gray-900 mb-2">{module.title}</h3>
                <p className="text-gray-600 mb-4">{module.description}</p>

                <div className="mb-4">
                  <h4 className="text-sm font-medium text-gray-700 mb-2">Lessons:</h4>
                  <ul className="space-y-1">
                    {module.lessons.map((lesson) => (
                      <li key={lesson.id} className="text-sm text-gray-600">
                        <Link
                          href={`/textbook-content/${lesson.id}`}
                          className="text-blue-600 hover:underline"
                        >
                          {lesson.title}
                        </Link>
                      </li>
                    ))}
                  </ul>
                </div>

                <Link
                  href={`/textbook-content/${module.id}`}
                  className="inline-block bg-blue-500 text-white px-4 py-2 rounded-lg text-sm hover:bg-blue-600"
                >
                  Start Module
                </Link>
              </div>
            </div>
          ))}
        </div>

        {/* Course Information */}
        <div className="mt-12">
          <h2 className="text-xl font-semibold text-gray-800 mb-4">Course Information</h2>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
            <Link href="/textbook-content/weekly_breakdown" className="bg-white p-4 rounded-lg shadow text-center hover:shadow-md">
              <h3 className="font-medium text-gray-900">Weekly Breakdown</h3>
            </Link>
            <Link href="/textbook-content/assessments" className="bg-white p-4 rounded-lg shadow text-center hover:shadow-md">
              <h3 className="font-medium text-gray-900">Assessments</h3>
            </Link>
            <Link href="/textbook-content/hardware" className="bg-white p-4 rounded-lg shadow text-center hover:shadow-md">
              <h3 className="font-medium text-gray-900">Hardware Guide</h3>
            </Link>
            <Link href="/textbook-content/capstone" className="bg-white p-4 rounded-lg shadow text-center hover:shadow-md">
              <h3 className="font-medium text-gray-900">Capstone Project</h3>
            </Link>
          </div>
        </div>
      </main>
    </div>
  );
}