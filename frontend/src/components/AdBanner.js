import React from 'react';
import { loadScript } from '../utils';

const AdBanner = () => {
  React.useEffect(() => {
    loadScript('https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-XXXXXX')
      .then(() => {
        (window.adsbygoogle = window.adsbygoogle || []).push({});
      });
  }, []);

  return (
    <ins className="adsbygoogle"
      style={{ display: 'block' }}
      data-ad-client="ca-pub-XXXXXX"
      data-ad-slot="1234567890"
      data-ad-format="auto"
      data-full-width-responsive="true"
    />
  );
};
