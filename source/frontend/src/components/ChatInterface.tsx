import React, { useState, useEffect, useRef } from 'react';
import { Send, Bot, User, Loader2, Settings, Database, Zap } from 'lucide-react';
import { io, Socket } from 'socket.io-client';

interface Message {
  id: string;
  content: string;
  sender: 'user' | 'ai';
  timestamp: string;
  type?: 'text' | 'campaign' | 'data';
}

interface DataSource {
  id: string;
  name: string;
  description: string;
  status: string;
  connected: boolean;
  available: boolean;
  real_data: boolean;
}

interface Campaign {
  campaign_id: string;
  name: string;
  description: string;
  channels: Array<{
    type: string;
    content: string;
    timing: string;
  }>;
  target_audience: {
    demographics: any;
    interests: string[];
    behavior: string[];
  };
}

const ChatInterface: React.FC = () => {
  const [messages, setMessages] = useState<Message[]>([]);
  const [inputMessage, setInputMessage] = useState('');
  const [isConnected, setIsConnected] = useState(false);
  const [isLoading, setIsLoading] = useState(false);
  const [dataSources, setDataSources] = useState<DataSource[]>([]);
  const [campaigns, setCampaigns] = useState<Campaign[]>([]);
  const [showDataSources, setShowDataSources] = useState(false);
  const [showCampaigns, setShowCampaigns] = useState(false);
  
  // Backend configuration
  const [config, setConfig] = useState<any>(null);
  const [configLoaded, setConfigLoaded] = useState(false);
  
  const socketRef = useRef<Socket | null>(null);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  const clientId = `client_${Date.now()}`;

  useEffect(() => {
    // Initialize WebSocket connection
    socketRef.current = io('ws://localhost:8000', {
      transports: ['websocket']
    });

    socketRef.current.on('connect', () => {
      setIsConnected(true);
      console.log('Connected to server');
    });

    socketRef.current.on('disconnect', () => {
      setIsConnected(false);
      console.log('Disconnected from server');
    });

    // Listen for AI responses
    socketRef.current.on('ai_response', (data: any) => {
      const newMessage: Message = {
        id: `msg_${Date.now()}`,
        content: data.content,
        sender: 'ai',
        timestamp: new Date().toISOString(),
        type: 'text'
      };
      setMessages(prev => [...prev, newMessage]);
      setIsLoading(false);
    });

    // Load configuration from backend first
    loadConfiguration();

    return () => {
      if (socketRef.current) {
        socketRef.current.disconnect();
      }
    };
  }, []);

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  const loadConfiguration = async () => {
    try {
      const apiUrl = import.meta.env.VITE_API_URL || 'http://localhost:8000';
      const response = await fetch(`${apiUrl}/api/config/`);
      const data = await response.json();
      
      if (data.success) {
        setConfig(data.configuration);
        setConfigLoaded(true);
        
        // Set data sources from backend configuration
        setDataSources(data.configuration.data_sources.map((source: any) => ({
          ...source,
          connected: false,
          status: 'disconnected'
        })));
      }
    } catch (error) {
      console.error('Error loading configuration:', error);
      // Fallback to default configuration
      setConfig({
        data_sources: [
          { id: 'google_ads', name: 'Google Ads', description: 'Google Ads data (Mock)', available: true, real_data: false },
          { id: 'facebook_pixel', name: 'Facebook Pixel', description: 'Facebook Pixel data (Mock)', available: true, real_data: false },
          { id: 'website', name: 'Website Analytics', description: 'Website data (Mock)', available: true, real_data: false }
        ],
        features: {
          real_data_sources: false,
          campaign_generation: true,
          websocket_chat: true
        }
      });
      setConfigLoaded(true);
    }
  };

  const loadDataSources = async () => {
    try {
      const response = await fetch('http://localhost:8000/api/data-sources/');
      const data = await response.json();
      setDataSources(data.sources.map((source: any) => ({
        ...source,
        connected: false
      })));
    } catch (error) {
      console.error('Error loading data sources:', error);
    }
  };

  const loadCampaigns = async () => {
    try {
      const response = await fetch(`http://localhost:8000/api/campaigns/history/${clientId}`);
      const data = await response.json();
      setCampaigns(data.campaigns || []);
    } catch (error) {
      console.error('Error loading campaigns:', error);
    }
  };

  const connectDataSource = async (sourceId: string) => {
    try {
      const response = await fetch(`http://localhost:8000/api/data-sources/connect/${sourceId}`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          api_key: `test_key_${sourceId}`,
          account_id: `test_account_${sourceId}`
        })
      });
      
      if (response.ok) {
        setDataSources(prev => prev.map(source => 
          source.id === sourceId ? { ...source, connected: true } : source
        ));
      }
    } catch (error) {
      console.error('Error connecting data source:', error);
    }
  };

  const sendMessage = async () => {
    if (!inputMessage.trim() || !socketRef.current) return;

    const userMessage: Message = {
      id: `msg_${Date.now()}`,
      content: inputMessage,
      sender: 'user',
      timestamp: new Date().toISOString(),
      type: 'text'
    };

    setMessages(prev => [...prev, userMessage]);
    setInputMessage('');
    setIsLoading(true);

    // Send message via WebSocket
    socketRef.current.emit('message', {
      type: 'chat_message',
      message: inputMessage,
      timestamp: new Date().toISOString()
    });

    // Check if message is about campaign generation (only if feature is enabled)
    if (config?.features?.campaign_generation && (inputMessage.toLowerCase().includes('campaign') || 
        inputMessage.toLowerCase().includes('create') ||
        inputMessage.toLowerCase().includes('generate'))) {
      
      // Generate campaign
      try {
        const connectedSources = dataSources.filter(ds => ds.connected);
        const response = await fetch('http://localhost:8000/api/campaigns/generate', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({
            message: inputMessage,
            data_sources: connectedSources.map(ds => ds.id),
            channels: ['email', 'sms', 'whatsapp', 'push'],
            client_id: clientId
          })
        });

        if (response.ok) {
          const data = await response.json();
          if (data.success) {
            const campaign = data.campaign;
            setCampaigns(prev => [campaign, ...prev]);
            
            const campaignMessage: Message = {
              id: `campaign_${Date.now()}`,
              content: `Campaign "${campaign.name}" generated successfully!`,
              sender: 'ai',
              timestamp: new Date().toISOString(),
              type: 'campaign'
            };
            setMessages(prev => [...prev, campaignMessage]);
          }
        }
      } catch (error) {
        console.error('Error generating campaign:', error);
      }
    }
  };

  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      sendMessage();
    }
  };

  return (
    <div className="flex flex-col h-[600px] bg-white rounded-lg shadow-lg overflow-hidden">
      {/* Header */}
      <div className="bg-gradient-to-r from-blue-600 to-indigo-600 text-white p-4 flex items-center justify-between">
        <div className="flex items-center space-x-2">
          <Bot className="w-6 h-6" />
          <h2 className="text-lg font-semibold">Perplexity Chat</h2>
        </div>
        <div className="flex items-center space-x-2">
          <button
            onClick={() => setShowDataSources(!showDataSources)}
            className="p-2 hover:bg-blue-700 rounded-lg transition-colors"
            title="Data Sources"
          >
            <Database className="w-5 h-5" />
          </button>
          <button
            onClick={() => setShowCampaigns(!showCampaigns)}
            className="p-2 hover:bg-blue-700 rounded-lg transition-colors"
            title="Campaigns"
          >
            <Zap className="w-5 h-5" />
          </button>
          <div className={`w-3 h-3 rounded-full ${isConnected ? 'bg-green-400' : 'bg-red-400'}`} />
        </div>
      </div>

      {/* Sidebar */}
      {(showDataSources || showCampaigns) && (
        <div className="flex-1 flex">
          <div className="w-80 bg-gray-50 border-r border-gray-200 p-4 overflow-y-auto">
            {showDataSources && (
              <div>
                <h3 className="text-lg font-semibold mb-4">Data Sources</h3>
                <div className="space-y-3">
                  {dataSources.map((source) => (
                    <div key={source.id} className="p-3 bg-white rounded-lg border">
                      <div className="flex items-center justify-between mb-2">
                        <h4 className="font-medium">{source.name}</h4>
                        <div className="flex items-center space-x-2">
                          {source.real_data && (
                            <span className="px-2 py-1 text-xs rounded bg-blue-100 text-blue-800">
                              Real Data
                            </span>
                          )}
                          <span className={`px-2 py-1 text-xs rounded ${
                            source.connected ? 'bg-green-100 text-green-800' : 'bg-gray-100 text-gray-600'
                          }`}>
                            {source.connected ? 'Connected' : 'Disconnected'}
                          </span>
                        </div>
                      </div>
                      <p className="text-sm text-gray-600 mb-2">{source.description}</p>
                      {!source.connected && (
                        <button
                          onClick={() => connectDataSource(source.id)}
                          className="w-full px-3 py-1 bg-blue-600 text-white text-sm rounded hover:bg-blue-700 transition-colors"
                        >
                          Connect
                        </button>
                      )}
                    </div>
                  ))}
                </div>
              </div>
            )}

            {showCampaigns && (
              <div>
                <h3 className="text-lg font-semibold mb-4">Campaigns</h3>
                <div className="space-y-3">
                  {campaigns.map((campaign) => (
                    <div key={campaign.campaign_id} className="p-3 bg-white rounded-lg border">
                      <h4 className="font-medium mb-1">{campaign.name}</h4>
                      <p className="text-sm text-gray-600 mb-2">{campaign.description}</p>
                      <div className="flex flex-wrap gap-1">
                        {campaign.channels.map((channel, index) => (
                          <span key={index} className="px-2 py-1 bg-blue-100 text-blue-800 text-xs rounded">
                            {channel.type}
                          </span>
                        ))}
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            )}
          </div>
        </div>
      )}

      {/* Messages */}
      <div className="flex-1 overflow-y-auto p-4 space-y-4">
        {messages.length === 0 && (
          <div className="text-center text-gray-500 py-8">
            <Bot className="w-12 h-12 mx-auto mb-4 text-gray-300" />
            <p>Start a conversation to create marketing campaigns!</p>
            <p className="text-sm mt-2">Try: "Create a campaign for cart abandoners"</p>
          </div>
        )}
        
        {messages.map((message) => (
          <div
            key={message.id}
            className={`flex ${message.sender === 'user' ? 'justify-end' : 'justify-start'}`}
          >
            <div
              className={`max-w-xs lg:max-w-md px-4 py-2 rounded-lg ${
                message.sender === 'user'
                  ? 'bg-blue-600 text-white'
                  : 'bg-gray-100 text-gray-900'
              }`}
            >
              <div className="flex items-center space-x-2 mb-1">
                {message.sender === 'ai' ? (
                  <Bot className="w-4 h-4" />
                ) : (
                  <User className="w-4 h-4" />
                )}
                <span className="text-xs opacity-70">
                  {new Date(message.timestamp).toLocaleTimeString()}
                </span>
              </div>
              <p className="text-sm">{message.content}</p>
            </div>
          </div>
        ))}
        
        {isLoading && (
          <div className="flex justify-start">
            <div className="bg-gray-100 px-4 py-2 rounded-lg flex items-center space-x-2">
              <Loader2 className="w-4 h-4 animate-spin" />
              <span className="text-sm text-gray-600">AI is thinking...</span>
            </div>
          </div>
        )}
        
        <div ref={messagesEndRef} />
      </div>

      {/* Input */}
      <div className="border-t border-gray-200 p-4">
        <div className="flex space-x-2">
          <input
            type="text"
            value={inputMessage}
            onChange={(e) => setInputMessage(e.target.value)}
            onKeyPress={handleKeyPress}
            placeholder="Ask me to create a marketing campaign..."
            className="flex-1 px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            disabled={!isConnected}
          />
          <button
            onClick={sendMessage}
            disabled={!inputMessage.trim() || !isConnected || isLoading}
            className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
          >
            <Send className="w-5 h-5" />
          </button>
        </div>
      </div>
    </div>
  );
};

export default ChatInterface;
