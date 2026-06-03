-- IFRI_MentorLink - schema SQL final
-- Base cible : MySQL 8+ / MariaDB compatible InnoDB
-- Ce fichier regroupe la structure finale des modules comptes, mentorat et messagerie.

SET FOREIGN_KEY_CHECKS = 0;

DROP TABLE IF EXISTS `messages`;
DROP TABLE IF EXISTS `conversations`;
DROP TABLE IF EXISTS `match_suggestions`;
DROP TABLE IF EXISTS `mentoring_requests`;
DROP TABLE IF EXISTS `user_skills`;
DROP TABLE IF EXISTS `user_availabilities`;
DROP TABLE IF EXISTS `users_user_permissions`;
DROP TABLE IF EXISTS `users_groups`;
DROP TABLE IF EXISTS `users`;
DROP TABLE IF EXISTS `skills`;
DROP TABLE IF EXISTS `fields_of_study`;

SET FOREIGN_KEY_CHECKS = 1;

CREATE TABLE `fields_of_study` (
    `id` BIGINT AUTO_INCREMENT NOT NULL,
    `nom` VARCHAR(100) NOT NULL,
    `description` LONGTEXT NOT NULL,
    PRIMARY KEY (`id`),
    UNIQUE KEY `fields_of_study_nom_uniq` (`nom`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE `skills` (
    `id` BIGINT AUTO_INCREMENT NOT NULL,
    `nom` VARCHAR(150) NOT NULL,
    `categorie` VARCHAR(100) NOT NULL,
    PRIMARY KEY (`id`),
    UNIQUE KEY `skills_nom_uniq` (`nom`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE `users` (
    `id` BIGINT AUTO_INCREMENT NOT NULL,
    `password` VARCHAR(128) NOT NULL,
    `last_login` DATETIME(6) NULL,
    `is_superuser` BOOLEAN NOT NULL DEFAULT FALSE,
    `nom` VARCHAR(100) NOT NULL,
    `prenom` VARCHAR(100) NOT NULL,
    `email` VARCHAR(254) NOT NULL,
    `telephone` VARCHAR(20) NOT NULL,
    `photo_profil` VARCHAR(100) NULL,
    `bio` LONGTEXT NOT NULL,
    `niveau` VARCHAR(10) NOT NULL,
    `role` VARCHAR(10) NOT NULL DEFAULT 'les_deux',
    `est_actif` BOOLEAN NOT NULL DEFAULT TRUE,
    `date_inscription` DATETIME(6) NOT NULL,
    `date_modification` DATETIME(6) NOT NULL,
    `token_reinitialisation` VARCHAR(255) NULL,
    `token_expire_le` DATETIME(6) NULL,
    `is_active` BOOLEAN NOT NULL DEFAULT TRUE,
    `is_staff` BOOLEAN NOT NULL DEFAULT FALSE,
    `filiere_id` BIGINT NULL,
    PRIMARY KEY (`id`),
    UNIQUE KEY `users_email_uniq` (`email`),
    UNIQUE KEY `users_telephone_uniq` (`telephone`),
    KEY `users_filiere_id_idx` (`filiere_id`),
    CONSTRAINT `users_filiere_id_fk`
        FOREIGN KEY (`filiere_id`) REFERENCES `fields_of_study` (`id`)
        ON DELETE SET NULL,
    CONSTRAINT `users_role_chk`
        CHECK (`role` IN ('mentor', 'mentore', 'les_deux')),
    CONSTRAINT `users_niveau_chk`
        CHECK (`niveau` IN ('', 'L1', 'L2', 'L3', 'M1', 'M2'))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE `users_groups` (
    `id` BIGINT AUTO_INCREMENT NOT NULL,
    `utilisateur_id` BIGINT NOT NULL,
    `group_id` INT NOT NULL,
    PRIMARY KEY (`id`),
    UNIQUE KEY `users_groups_utilisateur_group_uniq` (`utilisateur_id`, `group_id`),
    KEY `users_groups_group_id_idx` (`group_id`),
    CONSTRAINT `users_groups_utilisateur_id_fk`
        FOREIGN KEY (`utilisateur_id`) REFERENCES `users` (`id`)
        ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE `users_user_permissions` (
    `id` BIGINT AUTO_INCREMENT NOT NULL,
    `utilisateur_id` BIGINT NOT NULL,
    `permission_id` INT NOT NULL,
    PRIMARY KEY (`id`),
    UNIQUE KEY `users_permissions_utilisateur_permission_uniq` (`utilisateur_id`, `permission_id`),
    KEY `users_permissions_permission_id_idx` (`permission_id`),
    CONSTRAINT `users_permissions_utilisateur_id_fk`
        FOREIGN KEY (`utilisateur_id`) REFERENCES `users` (`id`)
        ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE `user_availabilities` (
    `id` BIGINT AUTO_INCREMENT NOT NULL,
    `jour` VARCHAR(10) NOT NULL,
    `heure_debut` TIME(6) NOT NULL,
    `heure_fin` TIME(6) NOT NULL,
    `utilisateur_id` BIGINT NOT NULL,
    PRIMARY KEY (`id`),
    KEY `user_availabilities_utilisateur_id_idx` (`utilisateur_id`),
    CONSTRAINT `user_availabilities_utilisateur_id_fk`
        FOREIGN KEY (`utilisateur_id`) REFERENCES `users` (`id`)
        ON DELETE CASCADE,
    CONSTRAINT `user_availabilities_jour_chk`
        CHECK (`jour` IN ('Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday')),
    CONSTRAINT `user_availabilities_hours_chk`
        CHECK (`heure_debut` < `heure_fin`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE `user_skills` (
    `id` BIGINT AUTO_INCREMENT NOT NULL,
    `type_competence` VARCHAR(10) NOT NULL,
    `niveau` SMALLINT UNSIGNED NOT NULL DEFAULT 3,
    `competence_id` BIGINT NOT NULL,
    `utilisateur_id` BIGINT NOT NULL,
    PRIMARY KEY (`id`),
    UNIQUE KEY `user_skills_utilisateur_competence_type_uniq` (`utilisateur_id`, `competence_id`, `type_competence`),
    KEY `user_skills_competence_id_idx` (`competence_id`),
    CONSTRAINT `user_skills_competence_id_fk`
        FOREIGN KEY (`competence_id`) REFERENCES `skills` (`id`)
        ON DELETE CASCADE,
    CONSTRAINT `user_skills_utilisateur_id_fk`
        FOREIGN KEY (`utilisateur_id`) REFERENCES `users` (`id`)
        ON DELETE CASCADE,
    CONSTRAINT `user_skills_type_chk`
        CHECK (`type_competence` IN ('force', 'lacune')),
    CONSTRAINT `user_skills_niveau_chk`
        CHECK (`niveau` BETWEEN 1 AND 5)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE `mentoring_requests` (
    `id` BIGINT AUTO_INCREMENT NOT NULL,
    `type_publication` VARCHAR(10) NOT NULL,
    `format_seance` VARCHAR(15) NOT NULL DEFAULT 'les_deux',
    `jour` VARCHAR(10) NULL,
    `heure_debut` TIME(6) NULL,
    `heure_fin` TIME(6) NULL,
    `description` LONGTEXT NOT NULL,
    `statut` VARCHAR(10) NOT NULL DEFAULT 'ouvert',
    `date_creation` DATETIME(6) NOT NULL,
    `date_modification` DATETIME(6) NOT NULL,
    `auteur_id` BIGINT NOT NULL,
    `competence_id` BIGINT NOT NULL,
    PRIMARY KEY (`id`),
    KEY `mentoring_requests_auteur_id_idx` (`auteur_id`),
    KEY `mentoring_requests_competence_id_idx` (`competence_id`),
    KEY `mentoring_requests_filters_idx` (`type_publication`, `statut`, `jour`),
    CONSTRAINT `mentoring_requests_auteur_id_fk`
        FOREIGN KEY (`auteur_id`) REFERENCES `users` (`id`)
        ON DELETE CASCADE,
    CONSTRAINT `mentoring_requests_competence_id_fk`
        FOREIGN KEY (`competence_id`) REFERENCES `skills` (`id`)
        ON DELETE CASCADE,
    CONSTRAINT `mentoring_requests_type_chk`
        CHECK (`type_publication` IN ('offre', 'demande')),
    CONSTRAINT `mentoring_requests_format_chk`
        CHECK (`format_seance` IN ('presentiel', 'en_ligne', 'les_deux')),
    CONSTRAINT `mentoring_requests_statut_chk`
        CHECK (`statut` IN ('ouvert', 'matche', 'ferme')),
    CONSTRAINT `mentoring_requests_jour_chk`
        CHECK (`jour` IS NULL OR `jour` IN ('Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday')),
    CONSTRAINT `mentoring_requests_hours_chk`
        CHECK (
            (`jour` IS NULL AND `heure_debut` IS NULL AND `heure_fin` IS NULL)
            OR (`jour` IS NOT NULL AND `heure_debut` IS NOT NULL AND `heure_fin` IS NOT NULL AND `heure_debut` < `heure_fin`)
        )
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE `match_suggestions` (
    `id` BIGINT AUTO_INCREMENT NOT NULL,
    `score_global` DECIMAL(5, 2) NOT NULL,
    `score_competences` DECIMAL(5, 2) NOT NULL DEFAULT 0,
    `score_horaires` DECIMAL(5, 2) NOT NULL DEFAULT 0,
    `score_filiere` DECIMAL(5, 2) NOT NULL DEFAULT 0,
    `statut` VARCHAR(15) NOT NULL DEFAULT 'en_attente',
    `date_creation` DATETIME(6) NOT NULL,
    `mentor_id` BIGINT NOT NULL,
    `mentore_id` BIGINT NOT NULL,
    PRIMARY KEY (`id`),
    UNIQUE KEY `match_suggestions_mentor_mentore_uniq` (`mentor_id`, `mentore_id`),
    KEY `match_suggestions_mentore_id_idx` (`mentore_id`),
    KEY `match_suggestions_score_idx` (`score_global`),
    CONSTRAINT `match_suggestions_mentor_id_fk`
        FOREIGN KEY (`mentor_id`) REFERENCES `users` (`id`)
        ON DELETE CASCADE,
    CONSTRAINT `match_suggestions_mentore_id_fk`
        FOREIGN KEY (`mentore_id`) REFERENCES `users` (`id`)
        ON DELETE CASCADE,
    CONSTRAINT `match_suggestions_statut_chk`
        CHECK (`statut` IN ('en_attente', 'accepte', 'refuse')),
    CONSTRAINT `match_suggestions_scores_chk`
        CHECK (
            `score_global` BETWEEN 0 AND 100
            AND `score_competences` BETWEEN 0 AND 100
            AND `score_horaires` BETWEEN 0 AND 100
            AND `score_filiere` BETWEEN 0 AND 100
        ),
    CONSTRAINT `match_suggestions_distinct_users_chk`
        CHECK (`mentor_id` <> `mentore_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE `conversations` (
    `id` BIGINT AUTO_INCREMENT NOT NULL,
    `date_creation` DATETIME(6) NOT NULL,
    `matching_id` BIGINT NULL,
    `utilisateur1_id` BIGINT NOT NULL,
    `utilisateur2_id` BIGINT NOT NULL,
    PRIMARY KEY (`id`),
    UNIQUE KEY `conversations_utilisateurs_uniq` (`utilisateur1_id`, `utilisateur2_id`),
    KEY `conversations_matching_id_idx` (`matching_id`),
    KEY `conversations_utilisateur2_id_idx` (`utilisateur2_id`),
    CONSTRAINT `conversations_matching_id_fk`
        FOREIGN KEY (`matching_id`) REFERENCES `match_suggestions` (`id`)
        ON DELETE SET NULL,
    CONSTRAINT `conversations_utilisateur1_id_fk`
        FOREIGN KEY (`utilisateur1_id`) REFERENCES `users` (`id`)
        ON DELETE CASCADE,
    CONSTRAINT `conversations_utilisateur2_id_fk`
        FOREIGN KEY (`utilisateur2_id`) REFERENCES `users` (`id`)
        ON DELETE CASCADE,
    CONSTRAINT `conversations_distinct_users_chk`
        CHECK (`utilisateur1_id` <> `utilisateur2_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE `messages` (
    `id` BIGINT AUTO_INCREMENT NOT NULL,
    `contenu` LONGTEXT NOT NULL,
    `lu` BOOLEAN NOT NULL DEFAULT FALSE,
    `date_envoi` DATETIME(6) NOT NULL,
    `conversation_id` BIGINT NOT NULL,
    `expediteur_id` BIGINT NOT NULL,
    PRIMARY KEY (`id`),
    KEY `messages_conversation_date_idx` (`conversation_id`, `date_envoi`),
    KEY `messages_expediteur_id_idx` (`expediteur_id`),
    CONSTRAINT `messages_conversation_id_fk`
        FOREIGN KEY (`conversation_id`) REFERENCES `conversations` (`id`)
        ON DELETE CASCADE,
    CONSTRAINT `messages_expediteur_id_fk`
        FOREIGN KEY (`expediteur_id`) REFERENCES `users` (`id`)
        ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
