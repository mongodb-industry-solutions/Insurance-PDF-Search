"use client";

import UserProfile from "../userProfile/UserProfile";
import styles from "./navbar.module.css";
import Image from "next/image";
import { useState } from "react";
import InfoWizard from "../InfoWizard/InfoWizard";

const Navbar = () => {
  const [openHelpModal, setOpenHelpModal] = useState(false);
  return (
    <nav className={styles.navbar}>
      <div className={styles.logo}>
        <Image src="/assets/logo.png" alt="Logo" width={200} height={40} />{" "}
      </div>
      <InfoWizard
          open={openHelpModal}
          setOpen={setOpenHelpModal}
          tooltipText="Tell me more!"
          iconGlyph="Wizard"
          sections={[
            {
              heading: "Instructions and Talk Track",
              content: [
                {
                  heading: "PDF Search",
                  body: "Retrieval-augmented generation (RAG) applications are a game changer for insurance companies, enabling them to harness the power of unstructured data while promoting accessibility and flexibility. Special attention goes to PDFs, which are ubiquitous yet difficult to search, leading claim adjusters and underwriters to spend hours reviewing contracts, claims, and guidelines in this common format. RAG for PDF search brings efficiency and accuracy to this historically cumbersome task. Now, users can simply type a question in natural language and the app will sift through the company data, provide an answer, summarize the content of the documents, and indicate the source of the information, including the page and paragraph where it was found.",
                },
                {
                  heading: "How to Demo",
                  body: [
                    "Click on one of the customer tabs, each customer is associated with a PDF corresponding to the insurance guidelines of Singapore or NYC, this highlights thepre-ltering capabilities of $vectorSearch.",
                    "Type a question or use the suggested ones",
                    "Press 'Ask'.",
                    "On the right we can see the section of the PDF where the information was found and that was used as context for the LLM. On the left there’s the answer elaborated by the LLM"
                  ],
                },
              ],
            },
            {
              heading: "Behind the Scenes",
              content: [
                {
                  heading: "Data Flow",
                  body: "",
                },
                {
                  images: [
                    {
                      src: "assets/ingest.png",
                      alt: "Ingest Architecture",
                    },
                    {
                      src: "assets/query.png",
                      alt: "Query Architecture",
                    },
                  ],
                },
              ],
            },
            {
              heading: "Why MongoDB?",
              content: [
                {
                  heading: "Operational and Vector database combined",
                  body: "MongoDB stores vectors alongside operational data, eliminating the need to having two separate solutions. Enabling features such as pre-filtering.",
                        
                },
                {
                  heading: "Flexibility",
                  body: "Easily store chunks and other PDF metadata.",
                }, 
                {
                  heading: "Performance",
                  body: "MongoDB's Vector Search is extremely fast at retrieving vectors.",
                        
                },
              ],
            },
          ]}
        />
      <div className={styles.user}>
        <UserProfile />
      </div>
    </nav>
  );
};

export default Navbar;
