import React, { useState } from 'react';
import styles from "./userProfile.module.css";

const UserProfile = () => {
    const [showAdditionalProfiles, setShowAdditionalProfiles] = useState(false);

    const toggleAdditionalProfiles = () => {
        setShowAdditionalProfiles(!showAdditionalProfiles);
    };

    return (
        <div>
            <div className={styles.profile} onClick={toggleAdditionalProfiles}>
                <div className={styles.imageContainer}>
                    <img
                        className={styles.image}
                        src="/eddie.png"
                        alt="User Profile"
                    />
                </div>
                <div className={styles.details}>
                    <div className={styles.name}>Eddie Grant</div>
                    <div className={styles.role}>Claim Adjuster</div>
                </div>
            </div>
            {showAdditionalProfiles && (
                <div className={styles.additionalProfilesContainer}>
                    <p>Switch user to:</p>
                    <AdditionalProfile name="Jane Tree" role="Underwriter" image="/jane.png" />
                    <AdditionalProfile name="Rob Smith" role="Customer" image="/rob.png" />
                </div>
            )}
        </div>
    );
};

const AdditionalProfile = ({ name, role, image }) => {
    return (
        <div className={styles.additionalProfile}>
            <div className={styles.imageContainer}>
                <img
                    className={styles.image}
                    src={image}
                    alt="User Profile"
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
