import Link from 'next/link';

export default function Home() {
  return (
    <div className="min-h-screen flex flex-col items-center justify-center bg-gray-50 p-4">
      <main className="max-w-md w-full bg-white rounded-2xl shadow-xl border border-gray-100 p-10 text-center transition-all duration-200">
        <div className="bg-indigo-50 w-16 h-16 rounded-full flex items-center justify-center mx-auto mb-6">
          <svg className="w-8 h-8 text-indigo-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z" />
          </svg>
        </div>
        
        <h1 className="text-3xl font-bold text-gray-900 mb-2 tracking-tight">
          Welcome to CRM Digital FTE
        </h1>
        <p className="text-gray-500 mb-8 text-lg">
          Your professional customer success and support portal.
        </p>
        
        <Link 
          href="/support"
          className="inline-flex w-full items-center justify-center py-4 px-6 bg-indigo-600 hover:bg-indigo-700 text-white font-bold rounded-xl shadow-lg shadow-indigo-100 hover:shadow-indigo-200 transition-all duration-200 active:scale-[0.98]"
        >
          Go to Support Portal
          <svg className="ml-2 w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M13 7l5 5m0 0l-5 5m5-5H6" />
          </svg>
        </Link>
      </main>
      
      <footer className="mt-12 text-gray-400 text-sm font-medium uppercase tracking-widest">
        &copy; 2026 CRM Digital FTE
      </footer>
    </div>
  );
}
