import { useState } from "react";
import Image from "next/image";
import styles from "./userProfile.module.css";

const UserProfile = () => {
  const [showAdditionalProfiles, setShowAdditionalProfiles] = useState(false);
  const [selectedProfile, setSelectedProfile] = useState({
    name: "Eddie Grant",
    role: "Claim Adjuster",
    image: "/assets/eddie.png",
  });

  const toggleAdditionalProfiles = () => {
    setShowAdditionalProfiles(!showAdditionalProfiles);
  };

  const switchProfile = (name, role, image) => {
    setSelectedProfile({ name, role, image });
    setShowAdditionalProfiles(false);
  };

  return (
    <div>
      <div className={styles.profile} onClick={toggleAdditionalProfiles}>
        <div className={styles.imageContainer}>
          <Image
            className={styles.image}
            src={selectedProfile.image}
            alt="User Profile"
            width={50}
            height={50}
          />
        </div>
        <div className={styles.details}>
          <div className={styles.name}>{selectedProfile.name}</div>
          <div className={styles.role}>{selectedProfile.role}</div>
        </div>
      </div>
      {showAdditionalProfiles && (
        <div className={styles.additionalProfilesContainer}>
          <p>Switch user to:</p>
          {selectedProfile.name !== "Jane Tree" && (
            <AdditionalProfile
              name="Jane Tree"
              role="Underwriter"
              image="/assets/jane.png"
              onClick={() =>
                switchProfile("Jane Tree", "Underwriter", "/assets/jane.png")
              }
            />
          )}
          {selectedProfile.name !== "Rob Smith" && (
            <AdditionalProfile
              name="Rob Smith"
              role="Customer Service"
              image="/assets/rob.png"
              onClick={() =>
                switchProfile(
                  "Rob Smith",
                  "Customer Service",
                  "/assets/rob.png"
                )
              }
            />
          )}
          {selectedProfile.name !== "Eddie Grant" && (
            <AdditionalProfile
              name="Eddie Grant"
              role="Claim Adjuster"
              image="/assets/eddie.png"
              onClick={() =>
                switchProfile(
                  "Eddie Grant",
                  "Claim Adjuster",
                  "/assets/eddie.png"
                )
              }
            />
          )}
        </div>
      )}
    </div>
  );
};

const AdditionalProfile = ({ name, role, image, onClick }) => {
  return (
    <div className={styles.additionalProfile} onClick={onClick}>
      <div className={styles.imageContainer}>
        <Image
          className={styles.image}
          src={image}
          alt="User Profile"
          width={50}
          height={50}
        />
      </div>
      <div className={styles.details}>
        <div className={styles.name}>{name}</div>
        <div className={styles.role}>{role}</div>
      </div>
    </div>
  );
};

export default UserProfile;
