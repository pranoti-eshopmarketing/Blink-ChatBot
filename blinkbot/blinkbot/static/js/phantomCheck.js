// phantomCheck.js

const getProvider = () => {
    if ('phantom' in window) {
      const provider = window.phantom?.solana;
  
      if (provider?.isPhantom) {
        console.log('Phantom wallet is available');
        // Here, you can redirect to a confirmation or a specific URL
        window.location.href = 'https://yourbotconfirmation.com/success';
        return provider;
      }
    }
  
    window.open('https://phantom.app/', '_blank');
    console.log('Phantom wallet is not available, redirecting to install');
  };
  
  // Immediately call getProvider when the script is loaded
  getProvider();
  