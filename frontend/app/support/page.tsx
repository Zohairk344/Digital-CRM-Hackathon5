import SupportForm from '../../components/SupportForm';

export default function SupportPage() {
  return (
    <main className="min-h-screen bg-slate-50 flex flex-col items-center justify-center py-12 px-4 sm:px-6 lg:px-8 transition-all duration-200">
      <div className="max-w-4xl w-full space-y-8">
        <div className="text-center">
          <h1 className="text-4xl font-bold text-slate-900 tracking-tight">
            Contact Customer Success
          </h1>
          <p className="mt-4 text-lg text-slate-500 max-w-2xl mx-auto">
            We&apos;re here to help you get the most out of our platform. Submit a request and our team will get back to you shortly.
          </p>
        </div>
        
        <div className="mt-10">
          <SupportForm />
        </div>
      </div>
    </main>
  );
}
