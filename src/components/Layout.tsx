import React, { ReactNode } from 'react';
import Head from 'next/head';
import Link from 'next/link';
import { useRouter } from 'next/router';

interface LayoutProps {
  children: ReactNode;
  title?: string;
}

const Layout = ({ children, title = 'Tally Subscriber Manager' }: LayoutProps) => {
  const router = useRouter();
  const [currentYear, setCurrentYear] = React.useState(new Date().getFullYear().toString());

  // Navigation items
  const navItems = [
    { href: '/', label: 'Dashboard' },
    { href: '/subscribers', label: 'Subscribers' },
    { href: '/newsletter', label: 'Send Newsletter' },
    { href: '/settings', label: 'Settings' },
  ];

  return (
    <>
      <Head>
        <title>{title}</title>
        <meta name="description" content="Manage subscribers from Tally forms and send newsletters" />
        <link rel="icon" href="/favicon.ico" />
      </Head>

      <div className="min-h-screen bg-gray-100">
        {/* Navigation */}
        <nav className="bg-white shadow-sm">
          <div className="container mx-auto">
            <div className="flex justify-between h-16">
              <div className="flex">
                <div className="flex-shrink-0 flex items-center">
                  <Link href="/" className="text-xl font-bold text-blue-600">
                    Tally Subscriber Manager
                  </Link>
                </div>
                <div className="hidden sm:ml-6 sm:flex sm:space-x-8">
                  {navItems.map((item) => (
                    <Link
                      key={item.href}
                      href={item.href}
                      className={`inline-flex items-center px-1 pt-1 border-b-2 text-sm font-medium ${
                        router.pathname === item.href
                          ? 'border-blue-500 text-gray-900'
                          : 'border-transparent text-gray-500 hover:border-gray-300 hover:text-gray-700'
                      }`}
                    >
                      {item.label}
                    </Link>
                  ))}
                </div>
              </div>
            </div>
          </div>
        </nav>

        {/* Main content */}
        <main className="py-10">
          <div className="container mx-auto">
            {children}
          </div>
        </main>

        {/* Footer */}
        <footer className="bg-white">
          <div className="container mx-auto py-6">
            <p className="text-center text-sm text-gray-500">
              &copy; {currentYear} Tally Subscriber Manager. All rights reserved.
            </p>
          </div>
        </footer>
      </div>
    </>
  );
};

export default Layout;
