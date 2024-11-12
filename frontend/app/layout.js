import { GeistSans } from "geist/font/sans";

export const metadata = {
  title: "Leafy Insurance",
  description: "",
};

export default function RootLayout({ children }) {
  return (
    <html lang="en" className={GeistSans.className}>
      <body>{children}</body>
    </html>
  );
}
