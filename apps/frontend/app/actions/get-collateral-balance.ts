"use server"

import axios from "axios"

export default async function getCollateralBalance(user: string, token: string) {
  try {
    const response = await axios.post("https://df68-203-215-167-42.ngrok-free.app/collateral-balance", {
      user,
      token,
    })
    return response.data
  } catch (error) {
    console.error("Failed to fetch collateral balance:", error)
    throw new Error("Could not fetch collateral balance")
  }
}
