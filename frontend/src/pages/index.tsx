import { useState, useEffect } from 'react';
import Layout from '../components/Layout';
import { getSubscribers, Subscriber } from '../utils/api';
import Link from 'next/link';

export default function Home() {
  const [subscribers, setSubscribers] = useState<Subscriber[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    const fetchData = async () => {
      try {
        setLoading(true);
        const data = await getSubscribers();
        setSubscribers(data);
        setError('');
      } catch (err) {
        console.error('Error fetching subscribers:', err);
        setError('Failed to load subscribers');
      } finally {
        setLoading(false);
      }
    };

    fetchData();
  }, []);

  // Removed webhook URL effect

  return (
    <Layout title="Dashboard - Tally Subscriber Manager">
      <div className="space-y-6">
        <div className="flex justify-between items-center">
          <h1 className="text-2xl font-bold text-gray-900">Dashboard</h1>
          <Link href="/newsletter" className="btn btn-primary">
            Send Newsletter
          </Link>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          {/* Subscribers count card */}
          <div className="card">
            <h2 className="text-lg font-medium text-gray-900">Total Subscribers</h2>
            <p className="mt-2 text-3xl font-bold text-blue-600">
              {loading ? '...' : subscribers.length}
            </p>
            <div className="mt-4">
              <Link href="/subscribers" className="text-sm text-blue-600 hover:text-blue-800">
                View all subscribers →
              </Link>
            </div>
          </div>

          {/* Quick actions card */}
          <div className="card">
            <h2 className="text-lg font-medium text-gray-900">Quick Actions</h2>
            <div className="mt-2 space-y-2">
              <Link href="/newsletter" className="block btn btn-primary w-full text-center">
                Send Newsletter
              </Link>
              <Link href="/subscribers" className="block btn btn-secondary w-full text-center">
                Manage Subscribers
              </Link>
              <Link href="/settings" className="block btn btn-secondary w-full text-center">
                Settings
              </Link>
            </div>
          </div>
        </div>

        {/* Recent subscribers */}
        <div className="card">
          <h2 className="text-lg font-medium text-gray-900">Recent Subscribers</h2>
          {loading ? (
            <p className="mt-2 text-gray-500">Loading subscribers...</p>
          ) : error ? (
            <p className="mt-2 text-red-500">{error}</p>
          ) : subscribers.length === 0 ? (
            <p className="mt-2 text-gray-500">No subscribers yet.</p>
          ) : (
            <div className="mt-4 overflow-x-auto">
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
                      Subscribed At
                    </th>
                  </tr>
                </thead>
                <tbody className="bg-white divide-y divide-gray-200">
                  {subscribers.slice(0, 5).map((subscriber) => (
                    <tr key={subscriber._id}>
                      <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">
                        {subscriber.email}
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                        {subscriber.name || '-'}
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                        {new Date(subscriber.subscribed_at).toLocaleDateString()}
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
              {subscribers.length > 5 && (
                <div className="mt-4 text-right">
                  <Link href="/subscribers" className="text-sm text-blue-600 hover:text-blue-800">
                    View all subscribers →
                  </Link>
                </div>
              )}
            </div>
          )}
        </div>
      </div>
    </Layout>
  );
}
