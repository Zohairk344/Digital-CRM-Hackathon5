'use client';

import React, { useState } from 'react';
import { useForm as useHookForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import * as z from 'zod';
import { 
  Send, 
  Loader2, 
  CheckCircle2, 
  AlertCircle, 
  User, 
  Mail, 
  Phone, 
  Tag, 
  MessageSquare 
} from 'lucide-react';

const formSchema = z.object({
  name: z.string().min(2, 'Name must be at least 2 characters'),
  email: z.string().email('Invalid email address'),
  phone: z.string().optional(),
  category: z.enum(['General', 'Bug Report', 'Feature Request', 'Billing']),
  priority: z.enum(['low', 'medium', 'high', 'urgent']),
  message: z.string().min(10, 'Message must be at least 10 characters'),
});

type FormData = z.infer<typeof formSchema>;

const SupportForm = () => {
  const [status, setStatus] = useState<'idle' | 'loading' | 'success' | 'error'>('idle');
  const [ticketId, setTicketId] = useState<string | null>(null);
  const [serverError, setServerError] = useState<string | null>(null);

  const {
    register,
    handleSubmit,
    reset,
    formState: { errors },
  } = useHookForm<FormData>({
    resolver: zodResolver(formSchema),
    defaultValues: {
      name: '',
      email: '',
      phone: '',
      category: 'General',
      priority: 'medium',
      message: '',
    },
  });

  const onSubmit = async (data: FormData) => {
    setStatus('loading');
    setServerError(null);

    try {
      const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';
      const response = await fetch(`${API_URL}/api/v1/webhooks/web-form`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(data),
      });

      const responseData = await response.json();

      if (!response.ok) {
        throw new Error(responseData.detail || 'Failed to submit form');
      }

      setTicketId(responseData.ticket_id);
      setStatus('success');
      reset();
    } catch (err: unknown) {
      const message = err instanceof Error ? err.message : 'An unexpected error occurred';
      setServerError(message);
      setStatus('error');
    }
  };

  if (status === 'success') {
    return (
      <div className="max-w-md mx-auto p-10 bg-white rounded-2xl shadow-xl border border-emerald-100 text-center transition-all duration-200 animate-in fade-in zoom-in-95">
        <div className="bg-emerald-50 w-20 h-20 rounded-full flex items-center justify-center mx-auto mb-6">
          <CheckCircle2 className="w-10 h-10 text-emerald-500" />
        </div>
        <h2 className="text-2xl font-bold text-slate-900 mb-2">Request Submitted!</h2>
        <p className="text-slate-500 mb-8">
          Thank you for reaching out. Your ticket has been created successfully and our team will review it shortly.
        </p>
        <div className="bg-slate-50 p-5 rounded-xl mb-8 border border-slate-100">
          <p className="text-xs text-slate-400 font-semibold uppercase tracking-widest mb-2">Ticket Reference</p>
          <p className="text-xl font-mono font-bold text-slate-800">{ticketId}</p>
        </div>
        <button
          onClick={() => setStatus('idle')}
          className="w-full py-4 px-6 bg-slate-900 hover:bg-slate-800 text-white font-semibold rounded-xl transition-all duration-200 active:scale-[0.98] shadow-lg shadow-slate-200"
        >
          Submit Another Request
        </button>
      </div>
    );
  }

  const inputClasses = (hasError: boolean) => `
    w-full pl-11 pr-4 py-3 rounded-lg border transition-all duration-200 outline-none
    ${hasError 
      ? 'border-red-300 focus:border-red-500 focus:ring-4 focus:ring-red-50' 
      : 'border-slate-200 focus:border-indigo-500 focus:ring-4 focus:ring-indigo-50'}
    text-slate-900 placeholder:text-slate-400 bg-white
  `;

  const labelClasses = "block text-sm font-semibold text-slate-700 mb-1.5";

  return (
    <div className="max-w-2xl mx-auto bg-white rounded-2xl shadow-xl border border-slate-100 overflow-hidden transition-all duration-200">
      <div className="p-8 sm:p-10">
        <form onSubmit={handleSubmit(onSubmit)} className="space-y-6">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div className="space-y-1">
              <label htmlFor="name" className={labelClasses}>Name *</label>
              <div className="relative">
                <User className="absolute left-3.5 top-1/2 -translate-y-1/2 w-5 h-5 text-slate-400" />
                <input
                  {...register('name')}
                  type="text"
                  id="name"
                  placeholder="John Doe"
                  className={inputClasses(!!errors.name)}
                />
              </div>
              {errors.name && <p className="text-xs text-red-600 font-medium mt-1">{errors.name.message}</p>}
            </div>
            
            <div className="space-y-1">
              <label htmlFor="email" className={labelClasses}>Email *</label>
              <div className="relative">
                <Mail className="absolute left-3.5 top-1/2 -translate-y-1/2 w-5 h-5 text-slate-400" />
                <input
                  {...register('email')}
                  type="email"
                  id="email"
                  placeholder="john@example.com"
                  className={inputClasses(!!errors.email)}
                />
              </div>
              {errors.email && <p className="text-xs text-red-600 font-medium mt-1">{errors.email.message}</p>}
            </div>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div className="space-y-1">
              <label htmlFor="phone" className={labelClasses}>Phone (Optional)</label>
              <div className="relative">
                <Phone className="absolute left-3.5 top-1/2 -translate-y-1/2 w-5 h-5 text-slate-400" />
                <input
                  {...register('phone')}
                  type="tel"
                  id="phone"
                  placeholder="+1 (555) 000-0000"
                  className={inputClasses(false)}
                />
              </div>
            </div>
            
            <div className="space-y-1">
              <label htmlFor="category" className={labelClasses}>Category *</label>
              <div className="relative">
                <Tag className="absolute left-3.5 top-1/2 -translate-y-1/2 w-5 h-5 text-slate-400 pointer-events-none" />
                <select
                  {...register('category')}
                  id="category"
                  className={`${inputClasses(false)} appearance-none`}
                >
                  <option value="General">General Inquiry</option>
                  <option value="Bug Report">Bug Report</option>
                  <option value="Feature Request">Feature Request</option>
                  <option value="Billing">Billing & Account</option>
                </select>
                <div className="absolute right-3 top-1/2 -translate-y-1/2 pointer-events-none">
                  <svg className="w-4 h-4 text-slate-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M19 9l-7 7-7-7" />
                  </svg>
                </div>
              </div>
            </div>
          </div>

          <div className="space-y-3">
            <label className={labelClasses}>Priority *</label>
            <div className="flex flex-wrap gap-3">
              {['low', 'medium', 'high', 'urgent'].map((p) => (
                <label key={p} className="flex-1 min-w-[100px] cursor-pointer group">
                  <input
                    {...register('priority')}
                    type="radio"
                    value={p}
                    className="sr-only peer"
                  />
                  <div className="px-4 py-2.5 text-center text-sm font-medium border rounded-xl border-slate-200 text-slate-600 bg-white peer-checked:bg-indigo-600 peer-checked:text-white peer-checked:border-indigo-600 transition-all duration-200 hover:border-indigo-200 group-active:scale-[0.97] capitalize">
                    {p}
                  </div>
                </label>
              ))}
            </div>
            {errors.priority && <p className="text-xs text-red-600 font-medium mt-1">{errors.priority.message}</p>}
          </div>

          <div className="space-y-1">
            <label htmlFor="message" className={labelClasses}>Message *</label>
            <div className="relative">
              <MessageSquare className="absolute left-3.5 top-4 w-5 h-5 text-slate-400" />
              <textarea
                {...register('message')}
                id="message"
                rows={4}
                placeholder="How can we help you today?"
                className={`${inputClasses(!!errors.message)} pt-3`}
              ></textarea>
            </div>
            {errors.message && <p className="text-xs text-red-600 font-medium mt-1">{errors.message.message}</p>}
          </div>

          {status === 'error' && (
            <div className="p-4 bg-red-50 border border-red-100 rounded-xl flex items-start space-x-3 text-red-800 animate-in slide-in-from-top-2 duration-300">
              <AlertCircle className="w-5 h-5 mt-0.5 flex-shrink-0 text-red-500" />
              <div>
                <p className="text-sm font-bold mb-0.5">Submission Error</p>
                <p className="text-sm opacity-90">{serverError}</p>
              </div>
            </div>
          )}

          <button
            type="submit"
            disabled={status === 'loading'}
            className="w-full py-4 px-6 bg-indigo-600 hover:bg-indigo-700 disabled:bg-indigo-400 disabled:cursor-not-allowed text-white font-bold rounded-xl shadow-lg shadow-indigo-100 hover:shadow-indigo-200 transition-all duration-200 flex items-center justify-center space-x-2 active:scale-[0.98]"
          >
            {status === 'loading' ? (
              <>
                <Loader2 className="w-5 h-5 animate-spin" />
                <span>Processing...</span>
              </>
            ) : (
              <>
                <Send className="w-5 h-5" />
                <span>Send Request</span>
              </>
            )}
          </button>
        </form>
      </div>
    </div>
  );
};

export default SupportForm;
