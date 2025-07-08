import React, { useEffect } from 'react';
import { loadScript } from '../utils';

const AdBanner = () => {
  useEffect(() => {
    const initializeAds = async () => {
      try {
        await loadScript('https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-XXXXXX');
        if (window.adsbygoogle) {
          window.adsbygoogle.push({});
        }
      } catch (error) {
        console.error('Ad script loading failed:', error);
      }
    };
    
    initializeAds();
  }, []);

  return (
    <div className="ad-banner">
      <ins className="adsbygoogle"
        style={{ display: 'block' }}
        data-ad-client="ca-pub-XXXXXX"
        data-ad-slot="1234567890"
        data-ad-format="auto"
        data-full-width-responsive="true"
      ></ins>
    </div>
  );
};

export default AdBanner;
