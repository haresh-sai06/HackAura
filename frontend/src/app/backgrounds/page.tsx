'use client';

import { useState, useEffect } from 'react';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Copy, Eye, Moon, Sun } from 'lucide-react';
import { ThemeToggle } from '@/components/ui/theme-toggle';

const backgrounds = [
  {
    name: 'Ocean Blue',
    class: 'bg-gradient-ocean',
    darkClass: 'bg-gradient-dark-ocean',
    description: 'Calming blue gradient reminiscent of ocean waters',
    css: 'background: linear-gradient(135deg, #e3f2fd 0%, #bbdefb 50%, #90caf9 100%);',
    darkCss: 'background: linear-gradient(135deg, #0d47a1 0%, #1565c0 50%, #1976d2 100%);'
  },
  {
    name: 'Mint Fresh',
    class: 'bg-gradient-mint',
    darkClass: 'bg-gradient-dark-mint',
    description: 'Refreshing mint green gradient',
    css: 'background: linear-gradient(135deg, #e8f5e8 0%, #c8e6c9 50%, #a5d6a7 100%);',
    darkCss: 'background: linear-gradient(135deg, #004d40 0%, #00695c 50%, #00796b 100%);'
  },
  {
    name: 'Soft Light',
    class: 'bg-gradient-light',
    darkClass: 'bg-gradient-dark-sunset',
    description: 'Warm peach and coral tones',
    css: 'background: linear-gradient(135deg, #ffecd2 0%, #fcb69f 100%);',
    darkCss: 'background: linear-gradient(135deg, #bf360c 0%, #d84315 50%, #e64a19 100%);'
  },
  {
    name: 'Lavender Dream',
    class: 'bg-gradient-blue',
    darkClass: 'bg-gradient-dark-purple',
    description: 'Soft purple and blue blend',
    css: 'background: linear-gradient(135deg, #e0c3fc 0%, #8ec5fc 100%);',
    darkCss: 'background: linear-gradient(135deg, #4a148c 0%, #6a1b9a 50%, #7b1fa2 100%);'
  },
  {
    name: 'Spring Green',
    class: 'bg-gradient-green',
    darkClass: 'bg-gradient-dark-green',
    description: 'Fresh spring green gradient',
    css: 'background: linear-gradient(135deg, #d4fc79 0%, #96e6a1 100%);',
    darkCss: 'background: linear-gradient(135deg, #1b5e20 0%, #2e7d32 50%, #43a047 100%);'
  },
  {
    name: 'Cotton Candy',
    class: 'bg-gradient-purple',
    darkClass: 'bg-gradient-dark-blue',
    description: 'Sweet pink and purple mix',
    css: 'background: linear-gradient(135deg, #a8edea 0%, #fed6e3 100%);',
    darkCss: 'background: linear-gradient(135deg, #1a237e 0%, #283593 50%, #3949ab 100%);'
  },
  {
    name: 'Sunset Glow',
    class: 'bg-gradient-sunset',
    darkClass: 'bg-gradient-dark-red',
    description: 'Warm sunset colors',
    css: 'background: linear-gradient(135deg, #ffecd2 0%, #fcb69f 50%, #ff8b94 100%);',
    darkCss: 'background: linear-gradient(135deg, #b71c1c 0%, #c62828 50%, #d32f2f 100%);'
  },
  {
    name: 'Dark Gray',
    class: 'bg-gradient-light-blue',
    darkClass: 'bg-gradient-dark-gray',
    description: 'Professional gray gradient',
    css: 'background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);',
    darkCss: 'background: linear-gradient(135deg, #263238 0%, #37474f 50%, #455a64 100%);'
  }
];

export default function BackgroundsPage() {
  const [selectedBg, setSelectedBg] = useState('bg-gradient-ocean');
  const [copiedCss, setCopiedCss] = useState('');
  const [isDark, setIsDark] = useState(false);

  useEffect(() => {
    const savedTheme = localStorage.getItem('theme');
    const systemPrefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
    
    if (savedTheme === 'dark' || (!savedTheme && systemPrefersDark)) {
      setIsDark(true);
      document.documentElement.classList.add('dark');
    }
  }, []);

  const copyToClipboard = (css: string, name: string) => {
    navigator.clipboard.writeText(css);
    setCopiedCss(name);
    setTimeout(() => setCopiedCss(''), 2000);
  };

  const toggleTheme = () => {
    const newIsDark = !isDark;
    setIsDark(newIsDark);
    
    if (newIsDark) {
      document.documentElement.classList.add('dark');
      localStorage.setItem('theme', 'dark');
    } else {
      document.documentElement.classList.remove('dark');
      localStorage.setItem('theme', 'light');
    }
  };

  const getBackgroundClass = (className: string) => {
    if (isDark) {
      const bg = backgrounds.find(b => b.class === className);
      return bg?.darkClass || className;
    }
    return className;
  };

  return (
    <div className={`min-h-screen p-8 ${getBackgroundClass(selectedBg)}`}>
      <div className="max-w-6xl mx-auto">
        <div className="text-center mb-8 flex items-center justify-between">
          <div>
            <h1 className={`text-4xl font-bold mb-4 ${isDark ? 'text-white' : 'text-gray-800'}`}>
              {isDark ? 'Dark' : 'Light'} Background Gallery
            </h1>
            <p className={`text-lg mb-6 ${isDark ? 'text-gray-300' : 'text-gray-600'}`}>
              Click on any background to preview it full screen
            </p>
          </div>
          <div className="flex items-center gap-4">
            <ThemeToggle />
            <Button
              variant="outline"
              onClick={toggleTheme}
              className="flex items-center gap-2"
            >
              {isDark ? <Sun className="h-4 w-4" /> : <Moon className="h-4 w-4" />}
              {isDark ? 'Light Mode' : 'Dark Mode'}
            </Button>
          </div>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {backgrounds.map((bg) => (
            <Card key={bg.name} className="overflow-hidden hover:shadow-lg transition-shadow">
              <div 
                className={`h-32 ${bg.class} cursor-pointer relative group`}
                onClick={() => setSelectedBg(bg.class)}
              >
                <div className="absolute inset-0 bg-black bg-opacity-0 group-hover:bg-opacity-20 transition-all flex items-center justify-center">
                  <Eye className="text-white opacity-0 group-hover:opacity-100 transition-opacity" size={24} />
                </div>
              </div>
              <CardHeader>
                <CardTitle className="text-lg">{bg.name}</CardTitle>
                <CardDescription>{bg.description}</CardDescription>
              </CardHeader>
              <CardContent>
                <div className="space-y-2">
                  <div className="p-2 bg-gray-100 rounded text-xs font-mono break-all">
                    {bg.css}
                  </div>
                  <Button
                    variant="outline"
                    size="sm"
                    className="w-full"
                    onClick={() => copyToClipboard(bg.css, bg.name)}
                  >
                    <Copy className="w-4 h-4 mr-2" />
                    {copiedCss === bg.name ? 'Copied!' : 'Copy CSS'}
                  </Button>
                </div>
              </CardContent>
            </Card>
          ))}
        </div>

        <div className="mt-12 text-center">
          <div className="inline-block p-6 bg-white bg-opacity-90 rounded-lg shadow-lg">
            <h2 className="text-2xl font-semibold mb-4">How to Use</h2>
            <div className="text-left space-y-2 text-sm">
              <p>1. Click on any background above to preview it</p>
              <p>2. Copy the CSS code using the "Copy CSS" button</p>
              <p>3. Apply it to your elements using the class name or CSS</p>
              <p>4. Available classes: <code className="bg-gray-100 px-2 py-1 rounded">bg-gradient-ocean</code>, <code className="bg-gray-100 px-2 py-1 rounded">bg-gradient-mint</code>, etc.</p>
            </div>
          </div>
        </div>

        <div className="mt-8 text-center">
          <Button 
            variant="outline" 
            onClick={() => setSelectedBg('bg-gradient-light-blue')}
            className="mr-2"
          >
            Reset to Default
          </Button>
          <Button 
            onClick={() => window.history.back()}
          >
            Go Back
          </Button>
        </div>
      </div>
    </div>
  );
}
