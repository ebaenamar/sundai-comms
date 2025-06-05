import { useState } from 'react';
import Layout from '../components/Layout';
import { toast } from 'react-toastify';

export default function SettingsPage() {
  const [webhookUrl, setWebhookUrl] = useState('');
  const [copied, setCopied] = useState(false);

  // Get the webhook URL
  useState(() => {
    if (typeof window !== 'undefined') {
      setWebhookUrl(`${window.location.origin}/api/webhook/tally`);
    }
  });

  const copyToClipboard = () => {
    navigator.clipboard.writeText(webhookUrl);
    setCopied(true);
    toast.success('Webhook URL copied to clipboard!');
    setTimeout(() => setCopied(false), 2000);
  };

  return (
    <Layout title="Settings - Tally Subscriber Manager">
      <div className="space-y-6">
        <div className="flex justify-between items-center">
          <h1 className="text-2xl font-bold text-gray-900">Settings</h1>
        </div>

        {/* Tally Integration Settings */}
        <div className="card">
          <h2 className="text-lg font-medium text-gray-900">Tally Integration</h2>
          <p className="mt-2 text-sm text-gray-500">
            Configure your Tally form to send submissions to this webhook URL.
          </p>

          <div className="mt-4">
            <label className="form-label">Webhook URL</label>
            <div className="mt-1 flex rounded-md shadow-sm">
              <input
                type="text"
                readOnly
                value={webhookUrl}
                className="flex-1 form-input rounded-none rounded-l-md"
              />
              <button
                type="button"
                onClick={copyToClipboard}
                className="inline-flex items-center px-3 rounded-r-md border border-l-0 border-gray-300 bg-gray-50 text-gray-500 hover:bg-gray-100"
              >
                {copied ? 'Copied!' : 'Copy'}
              </button>
            </div>
          </div>

          <div className="mt-6">
            <h3 className="text-md font-medium text-gray-900">How to set up your Tally webhook:</h3>
            <ol className="mt-2 space-y-2 text-sm text-gray-600 list-decimal pl-5">
              <li>Go to your Tally form dashboard</li>
              <li>Click on the form you want to connect</li>
              <li>Go to "Integrations" in the sidebar</li>
              <li>Select "Webhooks"</li>
              <li>Click "Connect"</li>
              <li>Paste the webhook URL shown above</li>
              <li>Optional: Add a signing secret for enhanced security</li>
              <li>Click "Save" to activate the webhook</li>
            </ol>
          </div>
        </div>

        {/* Email Settings */}
        <div className="card">
          <h2 className="text-lg font-medium text-gray-900">Email Settings</h2>
          <p className="mt-2 text-sm text-gray-500">
            Email settings are configured through environment variables.
          </p>

          <div className="mt-4">
            <h3 className="text-md font-medium text-gray-900">Required Environment Variables:</h3>
            <ul className="mt-2 space-y-2 text-sm text-gray-600 list-disc pl-5">
              <li><code className="bg-gray-100 px-1 py-0.5 rounded">GMAIL_ADDRESS</code>: Your Gmail address</li>
              <li><code className="bg-gray-100 px-1 py-0.5 rounded">GMAIL_APP_PASSWORD</code>: Your Gmail App Password</li>
            </ul>
          </div>

          <div className="mt-4">
            <p className="text-sm text-gray-500">
              These settings should be configured in your deployment environment or .env file.
            </p>
          </div>
        </div>

        {/* Database Settings */}
        <div className="card">
          <h2 className="text-lg font-medium text-gray-900">Database Settings</h2>
          <p className="mt-2 text-sm text-gray-500">
            Database connection is configured through environment variables.
          </p>

          <div className="mt-4">
            <h3 className="text-md font-medium text-gray-900">Required Environment Variables:</h3>
            <ul className="mt-2 space-y-2 text-sm text-gray-600 list-disc pl-5">
              <li><code className="bg-gray-100 px-1 py-0.5 rounded">MONGO_URI</code>: MongoDB connection string</li>
            </ul>
          </div>
        </div>
      </div>
    </Layout>
  );
}
