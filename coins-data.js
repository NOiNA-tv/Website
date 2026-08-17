// Client marks for the CLIENTS box on the SYS. INFO page. The bouncing
// "coin" cycles through these; a click swaps to a random different one.
//
// Each entry is { viewBox, inner } where `inner` is raw SVG markup rendered
// inside <svg fill="currentColor">, so shapes must not set their own fill.
//
// PLACEHOLDER: these are typeset wordmarks standing in for the real client
// logos. Drop in the actual vector marks (paths, same shape) when available.
export const COINS = [
  mark('Knesset', 'KNS'),
  mark('Channel 10', '10'),
  mark('Aiways', 'AIW'),
  mark('WRC', 'WRC'),
  mark('PayBox', 'PAY'),
  mark('Kan', 'KAN'),
  mark('Xealth', 'XEA'),
  mark('Vimeo', 'VIM'),
  mark('Discount', 'DSC'),
  mark('Bizzabo', 'BZB'),
  mark('yes', 'YES'),
  mark('Kido', 'KDO'),
  mark('Folo', 'FOLO'),
];

// A ring-enclosed monogram — reads at the 80px size the bouncer renders at.
function mark(name, short) {
  return {
    viewBox: '0 0 100 100',
    inner:
      '<circle cx="50" cy="50" r="46" fill="none" stroke="currentColor" stroke-width="4"/>' +
      '<text x="50" y="50" text-anchor="middle" dominant-baseline="central"' +
      ' font-family="\'Jersey 10\', monospace" font-size="' +
      (short.length > 3 ? 26 : 30) + '"' +
      ' letter-spacing="1">' + short + '</text>' +
      '<title>' + name + '</title>',
  };
}
