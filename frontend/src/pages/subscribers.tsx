import { useState, useEffect } from 'react';
import Layout from '../components/Layout';
import { getSubscribers, unsubscribe, Subscriber } from '../utils/api';
import { toast } from 'react-toastify';

export default function SubscribersPage() {
  const [subscribers, setSubscribers] = useState<Subscriber[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [showInactive, setShowInactive] = useState(false);

  const fetchSubscribers = async () => {
    try {
      setLoading(true);
      const data = await getSubscribers(!showInactive);
      setSubscribers(data);
      setError('');
    } catch (err) {
      console.error('Error fetching subscribers:', err);
      setError('Failed to load subscribers');
      toast.error('Failed to load subscribers');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchSubscribers();
  }, [showInactive]);

  const handleUnsubscribe = async (email: string) => {
    if (window.confirm(`Are you sure you want to unsubscribe ${email}?`)) {
      try {
        await unsubscribe(email);
        toast.success(`${email} has been unsubscribed`);
        fetchSubscribers();
      } catch (err) {
        console.error('Error unsubscribing:', err);
        toast.error('Failed to unsubscribe');
      }
    }
  };

  return (
    <Layout title="Subscribers - Tally Subscriber Manager">
      <div className="space-y-6">
        <div className="flex justify-between items-center">
          <h1 className="text-2xl font-bold text-gray-900">Subscribers</h1>
          <div className="flex items-center">
            <label className="inline-flex items-center mr-4">
              <input
                type="checkbox"
                className="form-checkbox h-5 w-5 text-blue-600"
                checked={showInactive}
                onChange={() => setShowInactive(!showInactive)}
              />
              <span className="ml-2 text-gray-700">Show Inactive</span>
            </label>
            <button
              onClick={fetchSubscribers}
              className="btn btn-secondary"
            >
              Refresh
            </button>
          </div>
        </div>

        {loading ? (
          <div className="text-center py-10">
            <p className="text-gray-500">Loading subscribers...</p>
          </div>
        ) : error ? (
          <div className="text-center py-10">
            <p className="text-red-500">{error}</p>
          </div>
        ) : subscribers.length === 0 ? (
          <div className="text-center py-10">
            <p className="text-gray-500">No subscribers found.</p>
          </div>
        ) : (
          <div className="card overflow-hidden">
            <div className="overflow-x-auto">
              <table className="min-w-full divide-y divide-gray-200">
                <thead className="bg-gray-50">
                  <tr>
                    <th scope="col" className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                      Email
                    </th>
                    <th scope="col" className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                      Name
                    </th>
                    <th scope="col" className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                      Status
                    </th>
                    <th scope="col" className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                      Subscribed At
                    </th>
                    <th scope="col" className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                      Actions
                    </th>
                  </tr>
                </thead>
                <tbody className="bg-white divide-y divide-gray-200">
                  {subscribers.map((subscriber) => (
                    <tr key={subscriber._id}>
                      <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">
                        {subscriber.email}
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                        {subscriber.name || '-'}
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                        <span className={`px-2 inline-flex text-xs leading-5 font-semibold rounded-full ${
                          subscriber.active ? 'bg-green-100 text-green-800' : 'bg-red-100 text-red-800'
                        }`}>
                          {subscriber.active ? 'Active' : 'Inactive'}
                        </span>
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                        {new Date(subscriber.subscribed_at).toLocaleDateString()}
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                        {subscriber.active && (
                          <button
                            onClick={() => handleUnsubscribe(subscriber.email)}
                            className="text-red-600 hover:text-red-900"
                          >
                            Unsubscribe
                          </button>
                        )}
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>
        )}
      </div>
    </Layout>
  );
}
