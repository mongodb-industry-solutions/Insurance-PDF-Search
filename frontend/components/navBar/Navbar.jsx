"use client";

import UserProfile from "../userProfile/UserProfile";
import styles from "./navbar.module.css";
import Image from "next/image";

const Navbar = () => {
  return (
    <nav className={styles.navbar}>
      <div className={styles.logo}>
        <Image src="/assets/logo.png" alt="Logo" width={250} height={55} />{" "}
      </div>
      <div className={styles.user}>
        <UserProfile />
      </div>
    </nav>
  );
};

export default Navbar;
