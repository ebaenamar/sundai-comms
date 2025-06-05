import { useState } from 'react';
import Layout from '../components/Layout';
import { sendNewsletter } from '../utils/api';
import { toast } from 'react-toastify';
import { useForm } from 'react-hook-form';

interface NewsletterForm {
  subject: string;
  content: string;
}

export default function NewsletterPage() {
  const [sending, setSending] = useState(false);
  const { register, handleSubmit, reset, formState: { errors } } = useForm<NewsletterForm>();

  const onSubmit = async (data: NewsletterForm) => {
    try {
      setSending(true);
      const result = await sendNewsletter(data.subject, data.content);
      toast.success(`Newsletter sent to ${result.recipients_count} subscribers!`);
      reset();
    } catch (err: any) {
      console.error('Error sending newsletter:', err);
      toast.error(err.response?.data?.error || 'Failed to send newsletter');
    } finally {
      setSending(false);
    }
  };

  return (
    <Layout title="Send Newsletter - Tally Subscriber Manager">
      <div className="space-y-6">
        <div className="flex justify-between items-center">
          <h1 className="text-2xl font-bold text-gray-900">Send Newsletter</h1>
        </div>

        <div className="card">
          <form onSubmit={handleSubmit(onSubmit)} className="space-y-6">
            <div>
              <label htmlFor="subject" className="form-label">
                Subject
              </label>
              <input
                id="subject"
                type="text"
                className={`form-input ${errors.subject ? 'border-red-500' : ''}`}
                placeholder="Newsletter Subject"
                {...register('subject', { required: 'Subject is required' })}
              />
              {errors.subject && (
                <p className="mt-1 text-sm text-red-600">{errors.subject.message}</p>
              )}
            </div>

            <div>
              <label htmlFor="content" className="form-label">
                Content
              </label>
              <textarea
                id="content"
                rows={10}
                className={`form-input ${errors.content ? 'border-red-500' : ''}`}
                placeholder="Write your newsletter content here..."
                {...register('content', { required: 'Content is required' })}
              ></textarea>
              {errors.content && (
                <p className="mt-1 text-sm text-red-600">{errors.content.message}</p>
              )}
            </div>

            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm text-gray-500">
                  This will send an email to all active subscribers.
                </p>
              </div>
              <div className="flex space-x-3">
                <button
                  type="button"
                  onClick={() => reset()}
                  className="btn btn-secondary"
                  disabled={sending}
                >
                  Clear
                </button>
                <button
                  type="submit"
                  className="btn btn-primary"
                  disabled={sending}
                >
                  {sending ? 'Sending...' : 'Send Newsletter'}
                </button>
              </div>
            </div>
          </form>
        </div>

        <div className="card">
          <h2 className="text-lg font-medium text-gray-900">Newsletter Tips</h2>
          <ul className="mt-4 space-y-2 text-sm text-gray-600 list-disc pl-5">
            <li>Keep your subject line clear and engaging</li>
            <li>Start with the most important information</li>
            <li>Use simple, direct language</li>
            <li>Include a clear call to action</li>
            <li>Proofread before sending</li>
          </ul>
        </div>
      </div>
    </Layout>
  );
}
